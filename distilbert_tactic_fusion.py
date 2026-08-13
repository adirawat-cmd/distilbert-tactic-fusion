import os
import random
import numpy as np
import pandas as pd
import torch

from torch import nn
from torch.utils.data import Dataset, DataLoader

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)
from sklearn.utils.class_weight import compute_class_weight

from transformers import (
    AutoTokenizer,
    DistilBertModel
)

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from semantic_groups import SEMANTIC_GROUPS


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_PATH = "merged_scam_dataset.csv"

DISTILBERT_NAME = "distilbert-base-uncased"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

MAX_LENGTH = 256

BATCH_SIZE = 8
EPOCHS = 3

LEARNING_RATE = 2e-5
TACTIC_LEARNING_RATE = 1e-4

RANDOM_STATE = 42

PATIENCE = 2

BEST_MODEL_PATH = "best_distilbert_tactic_fusion.pt"


# ============================================================
# REPRODUCIBILITY
# ============================================================

random.seed(RANDOM_STATE)
np.random.seed(RANDOM_STATE)
torch.manual_seed(RANDOM_STATE)

if torch.cuda.is_available():
    torch.cuda.manual_seed_all(RANDOM_STATE)


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("=" * 70)
print("DISTILBERT + TACTIC FEATURE FUSION")
print("=" * 70)

print()
print("Device:", DEVICE)

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))


# ============================================================
# LOAD DATASET
# ============================================================

print()
print("=" * 70)
print("LOADING DATASET")
print("=" * 70)

df = pd.read_csv(DATASET_PATH)

print("Dataset shape:", df.shape)

print()
print("Columns:")
print(df.columns.tolist())

print()
print("Label distribution:")
print(df["label"].value_counts())


texts = df["text"].astype(str).tolist()
labels = df["label"].astype(int).values


# ============================================================
# TRAIN / VALIDATION / TEST SPLIT
# ============================================================

print()
print("=" * 70)
print("TRAIN / VALIDATION / TEST SPLIT")
print("=" * 70)

# First: 80% train+validation, 20% test
train_val_texts, test_texts, train_val_labels, test_labels = train_test_split(
    texts,
    labels,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=labels
)

# Then: 80% train, 20% validation of the 80%
train_texts, val_texts, train_labels, val_labels = train_test_split(
    train_val_texts,
    train_val_labels,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=train_val_labels
)

print("Training samples  :", len(train_texts))
print("Validation samples:", len(val_texts))
print("Testing samples   :", len(test_texts))


# ============================================================
# LOAD DISTILBERT TOKENIZER
# ============================================================

print()
print("=" * 70)
print("LOADING PRETRAINED DISTILBERT TOKENIZER")
print("=" * 70)

tokenizer = AutoTokenizer.from_pretrained(
    DISTILBERT_NAME
)

print("Tokenizer loaded successfully.")


# ============================================================
# TOKENIZATION
# ============================================================

print()
print("Tokenizing datasets...")

train_encodings = tokenizer(
    train_texts,
    truncation=True,
    padding="max_length",
    max_length=MAX_LENGTH
)

val_encodings = tokenizer(
    val_texts,
    truncation=True,
    padding="max_length",
    max_length=MAX_LENGTH
)

test_encodings = tokenizer(
    test_texts,
    truncation=True,
    padding="max_length",
    max_length=MAX_LENGTH
)

print("Training input shape :", len(train_encodings["input_ids"]), MAX_LENGTH)
print("Validation input shape:", len(val_encodings["input_ids"]), MAX_LENGTH)
print("Testing input shape  :", len(test_encodings["input_ids"]), MAX_LENGTH)


# ============================================================
# PYTORCH DATASET
# ============================================================

class TextDataset(Dataset):

    def __init__(self, encodings, labels, tactic_features):
        self.encodings = encodings
        self.labels = labels
        self.tactic_features = tactic_features

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):

        item = {
            key: torch.tensor(
                value[idx],
                dtype=torch.long
            )
            for key, value in self.encodings.items()
        }

        item["labels"] = torch.tensor(
            self.labels[idx],
            dtype=torch.long
        )

        item["tactic_features"] = torch.tensor(
            self.tactic_features[idx],
            dtype=torch.float
        )

        return item


# ============================================================
# LOAD SENTENCE TRANSFORMER
# ============================================================

print()
print("=" * 70)
print("LOADING SEMANTIC TACTIC EMBEDDING MODEL")
print("=" * 70)

semantic_model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)

print("Semantic model loaded successfully.")
print(
    "Embedding dimension:",
    semantic_model.get_embedding_dimension()
)


# ============================================================
# PREPARE TACTIC VOCABULARY
# ============================================================

print()
print("=" * 70)
print("PREPARING TACTIC VOCABULARY")
print("=" * 70)

tactic_names = list(SEMANTIC_GROUPS.keys())

print("Number of tactics:", len(tactic_names))

group_embeddings = {}

for tactic, groups in SEMANTIC_GROUPS.items():

    group_embeddings[tactic] = {}

    for group_name, terms in groups.items():

        embeddings = semantic_model.encode(
            terms,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        group_embeddings[tactic][group_name] = {
            "terms": terms,
            "embeddings": embeddings
        }

print("Tactic vocabulary prepared.")


# ============================================================
# GENERATE TACTIC FEATURES
# ============================================================

def generate_tactic_features(text_list):

    """
    Generate one feature per tactic.

    For each tactic:
        1. Compare the input text embedding against
           all semantic-group seed terms.
        2. Take the highest cosine similarity.
        3. Use that value as the tactic feature.

    Output:
        numpy array of shape:
        (number_of_samples, 8)
    """

    print(
        "Generating embeddings for",
        len(text_list),
        "texts..."
    )

    text_embeddings = semantic_model.encode(
        text_list,
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=True
    )

    feature_matrix = []

    for i, text_embedding in enumerate(text_embeddings):

        tactic_scores = []

        for tactic in tactic_names:

            best_score = -1.0

            for group_name, data in group_embeddings[tactic].items():

                similarities = np.dot(
                    data["embeddings"],
                    text_embedding
                )

                group_best = float(
                    np.max(similarities)
                )

                if group_best > best_score:
                    best_score = group_best

            tactic_scores.append(best_score)

        feature_matrix.append(tactic_scores)

        if (i + 1) % 500 == 0 or (i + 1) == len(text_list):
            print(
                f"Processed {i + 1}/{len(text_list)}"
            )

    return np.array(
        feature_matrix,
        dtype=np.float32
    )


# ============================================================
# GENERATE FEATURES
# ============================================================

print()
print("=" * 70)
print("GENERATING TACTIC FEATURES")
print("=" * 70)

print()
print("Training tactic features:")

train_tactic_features = generate_tactic_features(
    train_texts
)

print()
print("Validation tactic features:")

val_tactic_features = generate_tactic_features(
    val_texts
)

print()
print("Testing tactic features:")

test_tactic_features = generate_tactic_features(
    test_texts
)

print()
print("Training tactic shape   :", train_tactic_features.shape)
print("Validation tactic shape :", val_tactic_features.shape)
print("Testing tactic shape    :", test_tactic_features.shape)

print()
print("Expected:")
print(
    "Training   :",
    (len(train_texts), len(tactic_names))
)
print(
    "Validation :",
    (len(val_texts), len(tactic_names))
)
print(
    "Testing    :",
    (len(test_texts), len(tactic_names))
)


# ============================================================
# SHOW SAMPLE TACTIC FEATURES
# ============================================================

print()
print("=" * 70)
print("SAMPLE TACTIC FEATURES")
print("=" * 70)

sample_df = pd.DataFrame(
    train_tactic_features[:5],
    columns=tactic_names
)

print(sample_df.round(4))


# ============================================================
# DATASETS AND DATALOADERS
# ============================================================

train_dataset = TextDataset(
    train_encodings,
    train_labels,
    train_tactic_features
)

val_dataset = TextDataset(
    val_encodings,
    val_labels,
    val_tactic_features
)

test_dataset = TextDataset(
    test_encodings,
    test_labels,
    test_tactic_features
)


train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False
)

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False
)

print()
print("DataLoaders created.")

print("Training batches  :", len(train_loader))
print("Validation batches:", len(val_loader))
print("Testing batches   :", len(test_loader))


# ============================================================
# CLASS WEIGHTS
# ============================================================

print()
print("=" * 70)
print("CLASS WEIGHTS")
print("=" * 70)

classes = np.array([0, 1])

weights = compute_class_weight(
    class_weight="balanced",
    classes=classes,
    y=train_labels
)

class_weights = torch.tensor(
    weights,
    dtype=torch.float
).to(DEVICE)

print(
    "Class weights:",
    {
        int(classes[i]): float(weights[i])
        for i in range(len(classes))
    }
)


# ============================================================
# MODEL
# ============================================================

class DistilBERTTacticFusion(nn.Module):

    def __init__(self):

        super().__init__()

        # ----------------------------------------------------
        # PRETRAINED DISTILBERT
        # ----------------------------------------------------

        self.distilbert = DistilBertModel.from_pretrained(
            DISTILBERT_NAME
        )

        hidden_size = self.distilbert.config.hidden_size

        # ----------------------------------------------------
        # TACTIC FEATURE PROCESSING
        # ----------------------------------------------------

        self.tactic_dense = nn.Sequential(

            nn.Linear(
                len(tactic_names),
                32
            ),

            nn.ReLU(),

            nn.Dropout(0.2)
        )

        # ----------------------------------------------------
        # FUSION CLASSIFIER
        # ----------------------------------------------------

        self.classifier = nn.Sequential(

            nn.Linear(
                hidden_size + 32,
                128
            ),

            nn.ReLU(),

            nn.Dropout(0.3),

            nn.Linear(
                128,
                2
            )
        )

    def forward(
        self,
        input_ids,
        attention_mask,
        tactic_features
    ):

        # ----------------------------------------------------
        # DISTILBERT REPRESENTATION
        # ----------------------------------------------------

        outputs = self.distilbert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        # DistilBERT does not have a traditional pooler.
        # We use the representation of the first token [CLS].

        text_representation = outputs.last_hidden_state[:, 0, :]

        # ----------------------------------------------------
        # TACTIC REPRESENTATION
        # ----------------------------------------------------

        tactic_representation = self.tactic_dense(
            tactic_features
        )

        # ----------------------------------------------------
        # FUSION
        # ----------------------------------------------------

        fused = torch.cat(
            [
                text_representation,
                tactic_representation
            ],
            dim=1
        )

        # ----------------------------------------------------
        # CLASSIFICATION
        # ----------------------------------------------------

        logits = self.classifier(
            fused
        )

        return logits


# ============================================================
# INITIALIZE MODEL
# ============================================================

print()
print("=" * 70)
print("LOADING PRETRAINED DISTILBERT + TACTIC FUSION MODEL")
print("=" * 70)

model = DistilBERTTacticFusion()

model = model.to(DEVICE)

total_parameters = sum(
    p.numel()
    for p in model.parameters()
)

trainable_parameters = sum(
    p.numel()
    for p in model.parameters()
    if p.requires_grad
)

print()
print("Total parameters    :", f"{total_parameters:,}")
print("Trainable parameters:", f"{trainable_parameters:,}")


# ============================================================
# LOSS
# ============================================================

criterion = nn.CrossEntropyLoss(
    weight=class_weights
)


# ============================================================
# OPTIMIZER
# ============================================================

optimizer = torch.optim.AdamW(
    [
        {
            "params": model.distilbert.parameters(),
            "lr": LEARNING_RATE
        },
        {
            "params": model.tactic_dense.parameters(),
            "lr": TACTIC_LEARNING_RATE
        },
        {
            "params": model.classifier.parameters(),
            "lr": TACTIC_LEARNING_RATE
        }
    ],
    weight_decay=0.01
)


# ============================================================
# EVALUATION FUNCTION
# ============================================================

def evaluate(model, dataloader):

    model.eval()

    total_loss = 0.0

    all_predictions = []
    all_labels = []

    with torch.no_grad():

        for batch in dataloader:

            input_ids = batch["input_ids"].to(DEVICE)
            attention_mask = batch["attention_mask"].to(DEVICE)

            tactic_features = batch[
                "tactic_features"
            ].to(DEVICE)

            labels_batch = batch[
                "labels"
            ].to(DEVICE)

            logits = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                tactic_features=tactic_features
            )

            loss = criterion(
                logits,
                labels_batch
            )

            total_loss += loss.item()

            predictions = torch.argmax(
                logits,
                dim=1
            )

            all_predictions.extend(
                predictions.cpu().numpy()
            )

            all_labels.extend(
                labels_batch.cpu().numpy()
            )

    avg_loss = total_loss / len(dataloader)

    accuracy = accuracy_score(
        all_labels,
        all_predictions
    )

    precision = precision_score(
        all_labels,
        all_predictions,
        zero_division=0
    )

    recall = recall_score(
        all_labels,
        all_predictions,
        zero_division=0
    )

    f1 = f1_score(
        all_labels,
        all_predictions,
        zero_division=0
    )

    return (
        avg_loss,
        accuracy,
        precision,
        recall,
        f1,
        all_labels,
        all_predictions
    )


# ============================================================
# TRAINING
# ============================================================

print()
print("=" * 70)
print("TRAINING")
print("=" * 70)

best_f1 = 0.0
patience_counter = 0

for epoch in range(EPOCHS):

    model.train()

    total_train_loss = 0.0

    for batch_index, batch in enumerate(train_loader):

        input_ids = batch["input_ids"].to(DEVICE)

        attention_mask = batch[
            "attention_mask"
        ].to(DEVICE)

        tactic_features = batch[
            "tactic_features"
        ].to(DEVICE)

        labels_batch = batch[
            "labels"
        ].to(DEVICE)

        optimizer.zero_grad()

        logits = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            tactic_features=tactic_features
        )

        loss = criterion(
            logits,
            labels_batch
        )

        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            model.parameters(),
            max_norm=1.0
        )

        optimizer.step()

        total_train_loss += loss.item()

        if (batch_index + 1) % 100 == 0:

            print(
                f"Epoch {epoch + 1}/{EPOCHS} "
                f"| Batch {batch_index + 1}/{len(train_loader)}"
            )

    avg_train_loss = (
        total_train_loss / len(train_loader)
    )

    (
        val_loss,
        val_accuracy,
        val_precision,
        val_recall,
        val_f1,
        _,
        _
    ) = evaluate(
        model,
        val_loader
    )

    print()
    print("-" * 70)
    print(f"Epoch {epoch + 1}/{EPOCHS}")

    print(
        f"Train Loss       : {avg_train_loss:.4f}"
    )

    print(
        f"Validation Loss  : {val_loss:.4f}"
    )

    print(
        f"Validation Acc   : {val_accuracy:.4f}"
    )

    print(
        f"Validation Prec  : {val_precision:.4f}"
    )

    print(
        f"Validation Recall: {val_recall:.4f}"
    )

    print(
        f"Validation F1    : {val_f1:.4f}"
    )

    print("-" * 70)

    # --------------------------------------------------------
    # SAVE BEST MODEL USING VALIDATION F1
    # --------------------------------------------------------

    if val_f1 > best_f1:

        best_f1 = val_f1

        patience_counter = 0

        torch.save(
            {
                "model_state_dict": model.state_dict(),
                "best_validation_f1": best_f1,
                "epoch": epoch + 1
            },
            BEST_MODEL_PATH
        )

        print(
            f"New best validation F1: {best_f1:.4f}"
        )

        print(
            "Best model saved."
        )

    else:

        patience_counter += 1

        print(
            f"Validation F1 did not improve."
        )

        print(
            f"Patience: {patience_counter}/{PATIENCE}"
        )

        if patience_counter >= PATIENCE:

            print(
                "Early stopping triggered."
            )

            break


# ============================================================
# LOAD BEST MODEL
# ============================================================

print()
print("=" * 70)
print("LOADING BEST MODEL")
print("=" * 70)

checkpoint = torch.load(
    BEST_MODEL_PATH,
    map_location=DEVICE
)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

print(
    "Best model loaded from:",
    BEST_MODEL_PATH
)

print(
    f"Best validation F1: "
    f"{checkpoint['best_validation_f1']:.4f}"
)

print(
    f"Best epoch: "
    f"{checkpoint['epoch']}"
)


# ============================================================
# FINAL TEST EVALUATION
# ============================================================

print()
print("=" * 70)
print("FINAL TEST EVALUATION")
print("=" * 70)

(
    test_loss,
    test_accuracy,
    test_precision,
    test_recall,
    test_f1,
    test_true,
    test_predictions
) = evaluate(
    model,
    test_loader
)

print()
print(
    f"Test Loss : {test_loss:.4f}"
)

print(
    f"Accuracy  : {test_accuracy:.4f}"
)

print(
    f"Precision : {test_precision:.4f}"
)

print(
    f"Recall    : {test_recall:.4f}"
)

print(
    f"F1 Score  : {test_f1:.4f}"
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print()
print("Classification Report:")

print(
    classification_report(
        test_true,
        test_predictions,
        target_names=[
            "Non-manipulative",
            "Manipulative"
        ],
        digits=2
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

print("Confusion Matrix:")

print(
    confusion_matrix(
        test_true,
        test_predictions
    )
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print()
print("=" * 70)
print("TRAINING COMPLETE")
print("=" * 70)

print()
print("Model: Pretrained DistilBERT + Semantic Tactic Features")

print(
    f"Best Validation F1: {checkpoint['best_validation_f1']:.4f}"
)

print(
    f"Final Test F1     : {test_f1:.4f}"
)

print()
print("Baseline comparison:")
print("Previous DistilBERT baseline F1: 0.8559")
print(
    f"DistilBERT + tactics F1        : {test_f1:.4f}"
)

print()
print(
    f"F1 improvement: "
    f"{test_f1 - 0.8559:+.4f}"
)

print("=" * 70)