
import json
import random
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from torch.utils.data import Dataset, DataLoader
from transformers import AutoModel, AutoTokenizer

from actual_system.safeconv_tactic_features import SAFEConvTacticFeatures


ROOT = Path(__file__).resolve().parent
TRAIN_CSV = ROOT / "SAFEConv_v2_2_PRIMARY_TRAIN.csv"
VAL_CSV = ROOT / "SAFEConv_v2_2_PRIMARY_VAL.csv"
OUTPUT = ROOT / "actual_system" / "safeconv_distilbert_bilstm_tactic_fusion.pt"

MODEL_NAME = "distilbert-base-uncased"
MAX_LENGTH = 128
MAX_TURNS = 16
BATCH_SIZE = 2
EPOCHS = 4
LEARNING_RATE = 2e-4
HIDDEN_SIZE = 256
NUM_TACTICS = 8
SEED = 42

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {DEVICE}")


def get_turns(text):
    """Split numbered or speaker-labelled conversations into turns."""
    import re

    text = str(text).strip()
    if not text:
        return [""]

    # Prefer numbered or explicitly speaker-labelled lines.
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) > 1:
        return lines[:MAX_TURNS]

    # Handle inline numbered turns such as '1. Person: ... 2. Person: ...'.
    pieces = re.split(r"(?<!\w)\s+(?=\d{1,2}[.)]\s+)", text)
    if len(pieces) > 1:
        return pieces[:MAX_TURNS]

    # Treat unstructured text as a single conversation turn.
    return [text]


def load_frame(path):
    df = pd.read_csv(path)

    text_column = "text_for_model" if "text_for_model" in df.columns else "text_masked"
    if text_column not in df.columns:
        raise ValueError(f"No supported text column in {path.name}")

    if "risk_label" not in df.columns:
        raise ValueError(f"'risk_label' is missing from {path.name}")

    df = df[[text_column, "risk_label"]].copy()
    df.columns = ["text", "label"]
    df["text"] = df["text"].fillna("").astype(str)
    df["label"] = pd.to_numeric(df["label"], errors="coerce")
    df = df.dropna(subset=["label"])
    df = df[df["label"].isin([0, 1])]
    df["label"] = df["label"].astype(int)
    df = df[df["text"].str.strip().ne("")]
    return df.reset_index(drop=True)


class ConversationDataset(Dataset):
    def __init__(self, frame, tokenizer, tactic_extractor):
        self.examples = []
        self.tokenizer = tokenizer

        cache_path = ROOT / (
            "train_tactic_features.npy"
            if frame.attrs.get("split") == "train"
            else "val_tactic_features.npy"
        )

        if cache_path.exists():
            features = np.load(cache_path)
            if len(features) != len(frame):
                raise ValueError(
                    f"{cache_path.name} row count does not match the dataset. "
                    "Delete the stale cache and rerun."
                )
            print(f"Loaded cached features: {cache_path.name}")
        else:
            print(f"Computing tactic features for {len(frame)} conversations...")
            features = np.stack([
                tactic_extractor.transform(text)
                for text in frame["text"].tolist()
            ]).astype(np.float32)
            np.save(cache_path, features)
            print(f"Saved: {cache_path.name}")

        for text, label, tactic_features in zip(
            frame["text"], frame["label"], features
        ):
            turns = get_turns(text)
            turns = turns[-MAX_TURNS:]

            self.examples.append({
                "turns": turns,
                "label": int(label),
                "tactics": tactic_features,
            })

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, index):
        item = self.examples[index]
        encoded = self.tokenizer(
            item["turns"],
            padding="max_length",
            truncation=True,
            max_length=MAX_LENGTH,
            return_tensors="pt",
        )

        return {
            "input_ids": encoded["input_ids"],
            "attention_mask": encoded["attention_mask"],
            "tactics": torch.tensor(item["tactics"], dtype=torch.float32),
            "label": torch.tensor(item["label"], dtype=torch.long),
        }


class SAFEConvFusionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(MODEL_NAME)

        # Freeze DistilBERT initially to fit the available GPU memory.
        for parameter in self.encoder.parameters():
            parameter.requires_grad = False

        self.lstm = nn.LSTM(
            input_size=768,
            hidden_size=HIDDEN_SIZE,
            batch_first=True,
            bidirectional=True,
        )

        self.tactic_dense = nn.Sequential(
            nn.Linear(NUM_TACTICS, 32),
            nn.ReLU(),
        )

        self.classifier = nn.Sequential(
            nn.Linear(HIDDEN_SIZE * 2 + 32, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 2),
        )

    def forward(self, input_ids, attention_mask, tactics):
        # Shape: batch, turns, tokens
        batch_size, turns, tokens = input_ids.shape

        flat_ids = input_ids.reshape(-1, tokens)
        flat_mask = attention_mask.reshape(-1, tokens)

        with torch.no_grad():
            outputs = self.encoder(
                input_ids=flat_ids,
                attention_mask=flat_mask,
            )
            cls_vectors = outputs.last_hidden_state[:, 0, :]

        cls_vectors = cls_vectors.reshape(batch_size, turns, -1)

        # A turn is valid if it contains at least one attended token.
        valid_turns = attention_mask.sum(dim=-1).squeeze(-1).gt(0)

        sequence_output, _ = self.lstm(cls_vectors)

        mask = valid_turns.unsqueeze(-1).to(sequence_output.dtype)
        conversation_vector = (sequence_output * mask).sum(dim=1)
        conversation_vector = conversation_vector / mask.sum(dim=1).clamp(min=1)

        tactic_vector = self.tactic_dense(tactics)
        combined = torch.cat([conversation_vector, tactic_vector], dim=1)

        return self.classifier(combined)


def evaluate(model, loader):
    model.eval()
    all_labels, all_predictions = [], []

    with torch.no_grad():
        for batch in loader:
            ids = batch["input_ids"].to(DEVICE)
            masks = batch["attention_mask"].to(DEVICE)
            tactics = batch["tactics"].to(DEVICE)
            labels = batch["label"].to(DEVICE)

            logits = model(ids, masks, tactics)
            predictions = logits.argmax(dim=1)

            all_labels.extend(labels.cpu().tolist())
            all_predictions.extend(predictions.cpu().tolist())

    accuracy = accuracy_score(all_labels, all_predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(
        all_labels,
        all_predictions,
        average="binary",
        zero_division=0,
    )
    return accuracy, precision, recall, f1


def main():
    if not TRAIN_CSV.exists() or not VAL_CSV.exists():
        raise FileNotFoundError(
            "Expected train/validation CSV files in the project root."
        )

    train_frame = load_frame(TRAIN_CSV)
    val_frame = load_frame(VAL_CSV)
    train_frame.attrs["split"] = "train"
    val_frame.attrs["split"] = "val"

    print(f"Training rows: {len(train_frame)}")
    print(f"Validation rows: {len(val_frame)}")
    print("Training labels:", train_frame["label"].value_counts().to_dict())
    print("Validation labels:", val_frame["label"].value_counts().to_dict())

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tactic_extractor = SAFEConvTacticFeatures()

    train_dataset = ConversationDataset(
        train_frame, tokenizer, tactic_extractor
    )
    val_dataset = ConversationDataset(
        val_frame, tokenizer, tactic_extractor
    )

    train_loader = DataLoader(
        train_dataset, batch_size=BATCH_SIZE, shuffle=True
    )
    val_loader = DataLoader(
        val_dataset, batch_size=BATCH_SIZE, shuffle=False
    )

    model = SAFEConvFusionModel().to(DEVICE)

    labels = train_frame["label"].to_numpy()
    counts = np.bincount(labels, minlength=2)
    class_weights = len(labels) / (2.0 * np.maximum(counts, 1))
    criterion = nn.CrossEntropyLoss(
        weight=torch.tensor(class_weights, dtype=torch.float32, device=DEVICE)
    )

    optimizer = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad],
        lr=LEARNING_RATE,
    )

    best_f1 = -1.0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0.0

        for step, batch in enumerate(train_loader, start=1):
            ids = batch["input_ids"].to(DEVICE)
            masks = batch["attention_mask"].to(DEVICE)
            tactics = batch["tactics"].to(DEVICE)
            labels = batch["label"].to(DEVICE)

            optimizer.zero_grad(set_to_none=True)
            logits = model(ids, masks, tactics)
            loss = criterion(logits, labels)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(
                [p for p in model.parameters() if p.requires_grad], 1.0
            )
            optimizer.step()
            total_loss += loss.item()

            if step % 100 == 0:
                print(
                    f"Epoch {epoch + 1}/{EPOCHS} | "
                    f"Step {step}/{len(train_loader)} | "
                    f"Loss {loss.item():.4f}"
                )

        metrics = evaluate(model, val_loader)
        accuracy, precision, recall, f1 = metrics

        print(
            f"\nEpoch {epoch + 1}: "
            f"loss={total_loss / max(len(train_loader), 1):.4f}, "
            f"accuracy={accuracy:.4f}, precision={precision:.4f}, "
            f"recall={recall:.4f}, F1={f1:.4f}\n"
        )

        if f1 > best_f1:
            best_f1 = f1
            torch.save({
                "model_state_dict": model.state_dict(),
                "epoch": epoch + 1,
                "best_validation_f1": best_f1,
                "config": {
                    "model_name": MODEL_NAME,
                    "max_length": MAX_LENGTH,
                    "max_turns": MAX_TURNS,
                    "hidden_size": HIDDEN_SIZE,
                    "tactic_order": SAFEConvTacticFeatures.TACTIC_ORDER,
                    "threshold": 0.46,
                    "architecture": "DistilBERT-BiLSTM-tactic-fusion",
                },
            }, OUTPUT)
            print(f"Saved best checkpoint: {OUTPUT}")

    print(f"\nTraining finished. Best validation F1: {best_f1:.4f}")
    print("Next step: connect this checkpoint to inference.")


if __name__ == "__main__":
    main()