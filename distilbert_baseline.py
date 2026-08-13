# import os
# import random
# import numpy as np
# import pandas as pd
# import torch

# from sklearn.model_selection import train_test_split
# from sklearn.metrics import (
#     accuracy_score,
#     precision_score,
#     recall_score,
#     f1_score,
#     classification_report,
#     confusion_matrix
# )
# from sklearn.utils.class_weight import compute_class_weight

# from torch.utils.data import Dataset, DataLoader
# from torch.optim import AdamW

# from transformers import (
#     AutoTokenizer,
#     AutoModelForSequenceClassification
# )


# # ============================================================
# # CONFIGURATION
# # ============================================================

# DATASET_PATH = "merged_scam_dataset.csv"

# MODEL_NAME = "distilbert-base-uncased"

# MAX_LENGTH = 256

# BATCH_SIZE = 8

# EPOCHS = 3

# LEARNING_RATE = 2e-5

# RANDOM_STATE = 42

# DEVICE = torch.device(
#     "cuda" if torch.cuda.is_available() else "cpu"
# )


# # ============================================================
# # REPRODUCIBILITY
# # ============================================================

# random.seed(RANDOM_STATE)
# np.random.seed(RANDOM_STATE)
# torch.manual_seed(RANDOM_STATE)


# # ============================================================
# # DEVICE
# # ============================================================

# print("=" * 70)
# print("DISTILBERT BASELINE")
# print("=" * 70)

# print("\nDevice:", DEVICE)

# if torch.cuda.is_available():
#     print(
#         "GPU:",
#         torch.cuda.get_device_name(0)
#     )
# else:
#     print("GPU not available. Running on CPU.")


# # ============================================================
# # LOAD DATA
# # ============================================================

# print("\n" + "=" * 70)
# print("LOADING DATASET")
# print("=" * 70)

# df = pd.read_csv(DATASET_PATH)

# df = df.dropna(
#     subset=["text", "label"]
# ).reset_index(drop=True)

# df["text"] = df["text"].astype(str)
# df["label"] = df["label"].astype(int)

# print("Dataset shape:", df.shape)

# print("\nLabel distribution:")
# print(df["label"].value_counts())


# texts = df["text"].to_numpy()
# labels = df["label"].to_numpy()


# # ============================================================
# # TRAIN / TEST SPLIT
# # ============================================================

# print("\n" + "=" * 70)
# print("TRAIN / TEST SPLIT")
# print("=" * 70)

# (
#     text_train_full,
#     text_test,
#     y_train_full,
#     y_test
# ) = train_test_split(
#     texts,
#     labels,
#     test_size=0.20,
#     random_state=RANDOM_STATE,
#     stratify=labels
# )


# # ============================================================
# # TRAIN / VALIDATION SPLIT
# # ============================================================

# (
#     text_train,
#     text_val,
#     y_train,
#     y_val
# ) = train_test_split(
#     text_train_full,
#     y_train_full,
#     test_size=0.20,
#     random_state=RANDOM_STATE,
#     stratify=y_train_full
# )

# print("Training samples  :", len(text_train))
# print("Validation samples:", len(text_val))
# print("Testing samples   :", len(text_test))


# # ============================================================
# # TOKENIZER
# # ============================================================

# print("\n" + "=" * 70)
# print("LOADING PRETRAINED DISTILBERT TOKENIZER")
# print("=" * 70)

# tokenizer = AutoTokenizer.from_pretrained(
#     MODEL_NAME
# )

# print("Tokenizer loaded successfully.")


# # ============================================================
# # DATASET CLASS
# # ============================================================

# class ManipulationDataset(Dataset):

#     def __init__(
#         self,
#         texts,
#         labels,
#         tokenizer,
#         max_length
#     ):

#         self.texts = texts
#         self.labels = labels
#         self.tokenizer = tokenizer
#         self.max_length = max_length

#     def __len__(self):

#         return len(self.texts)

#     def __getitem__(self, index):

#         text = self.texts[index]
#         label = self.labels[index]

#         encoding = self.tokenizer(
#             text,
#             truncation=True,
#             padding="max_length",
#             max_length=self.max_length,
#             return_tensors="pt"
#         )

#         item = {
#             "input_ids": encoding["input_ids"].squeeze(0),
#             "attention_mask": encoding["attention_mask"].squeeze(0),
#             "labels": torch.tensor(
#                 label,
#                 dtype=torch.long
#             )
#         }

#         return item


# # ============================================================
# # CREATE DATASETS
# # ============================================================

# train_dataset = ManipulationDataset(
#     text_train,
#     y_train,
#     tokenizer,
#     MAX_LENGTH
# )

# val_dataset = ManipulationDataset(
#     text_val,
#     y_val,
#     tokenizer,
#     MAX_LENGTH
# )

# test_dataset = ManipulationDataset(
#     text_test,
#     y_test,
#     tokenizer,
#     MAX_LENGTH
# )


# # ============================================================
# # DATA LOADERS
# # ============================================================

# train_loader = DataLoader(
#     train_dataset,
#     batch_size=BATCH_SIZE,
#     shuffle=True
# )

# val_loader = DataLoader(
#     val_dataset,
#     batch_size=BATCH_SIZE,
#     shuffle=False
# )

# test_loader = DataLoader(
#     test_dataset,
#     batch_size=BATCH_SIZE,
#     shuffle=False
# )

# print("\nDataLoaders created.")

# print(
#     "Training batches  :",
#     len(train_loader)
# )

# print(
#     "Validation batches:",
#     len(val_loader)
# )

# print(
#     "Testing batches   :",
#     len(test_loader)
# )


# # ============================================================
# # CLASS WEIGHTS
# # ============================================================

# print("\n" + "=" * 70)
# print("CLASS WEIGHTS")
# print("=" * 70)

# classes = np.unique(y_train)

# weights = compute_class_weight(
#     class_weight="balanced",
#     classes=classes,
#     y=y_train
# )

# class_weights = torch.tensor(
#     weights,
#     dtype=torch.float
# ).to(DEVICE)

# print(
#     "Class weights:",
#     {
#         int(cls): float(weight)
#         for cls, weight in zip(classes, weights)
#     }
# )


# # ============================================================
# # LOAD PRETRAINED DISTILBERT
# # ============================================================

# print("\n" + "=" * 70)
# print("LOADING PRETRAINED DISTILBERT")
# print("=" * 70)

# model = AutoModelForSequenceClassification.from_pretrained(
#     MODEL_NAME,
#     num_labels=2
# )

# model.to(DEVICE)

# print("DistilBERT loaded successfully.")


# # ============================================================
# # MODEL INFORMATION
# # ============================================================

# total_parameters = sum(
#     p.numel()
#     for p in model.parameters()
# )

# trainable_parameters = sum(
#     p.numel()
#     for p in model.parameters()
#     if p.requires_grad
# )

# print(
#     "\nTotal parameters:",
#     f"{total_parameters:,}"
# )

# print(
#     "Trainable parameters:",
#     f"{trainable_parameters:,}"
# )


# # ============================================================
# # OPTIMIZER
# # ============================================================

# optimizer = AdamW(
#     model.parameters(),
#     lr=LEARNING_RATE
# )


# # ============================================================
# # LOSS FUNCTION
# # ============================================================

# criterion = torch.nn.CrossEntropyLoss(
#     weight=class_weights
# )


# # ============================================================
# # EVALUATION FUNCTION
# # ============================================================

# def evaluate(model, loader):

#     model.eval()

#     total_loss = 0

#     predictions = []
#     actual_labels = []

#     with torch.no_grad():

#         for batch in loader:

#             input_ids = batch[
#                 "input_ids"
#             ].to(DEVICE)

#             attention_mask = batch[
#                 "attention_mask"
#             ].to(DEVICE)

#             labels_batch = batch[
#                 "labels"
#             ].to(DEVICE)

#             outputs = model(
#                 input_ids=input_ids,
#                 attention_mask=attention_mask
#             )

#             logits = outputs.logits

#             loss = criterion(
#                 logits,
#                 labels_batch
#             )

#             total_loss += loss.item()

#             preds = torch.argmax(
#                 logits,
#                 dim=1
#             )

#             predictions.extend(
#                 preds.cpu().numpy()
#             )

#             actual_labels.extend(
#                 labels_batch.cpu().numpy()
#             )

#     average_loss = (
#         total_loss / len(loader)
#     )

#     accuracy = accuracy_score(
#         actual_labels,
#         predictions
#     )

#     precision = precision_score(
#         actual_labels,
#         predictions,
#         zero_division=0
#     )

#     recall = recall_score(
#         actual_labels,
#         predictions,
#         zero_division=0
#     )

#     f1 = f1_score(
#         actual_labels,
#         predictions,
#         zero_division=0
#     )

#     return (
#         average_loss,
#         accuracy,
#         precision,
#         recall,
#         f1,
#         actual_labels,
#         predictions
#     )


# # ============================================================
# # TRAINING
# # ============================================================

# print("\n" + "=" * 70)
# print("TRAINING DISTILBERT")
# print("=" * 70)

# best_val_loss = float("inf")

# patience = 1
# epochs_without_improvement = 0

# best_model_path = "best_distilbert_baseline.pt"


# for epoch in range(EPOCHS):

#     model.train()

#     total_train_loss = 0

#     for batch_index, batch in enumerate(
#         train_loader
#     ):

#         input_ids = batch[
#             "input_ids"
#         ].to(DEVICE)

#         attention_mask = batch[
#             "attention_mask"
#         ].to(DEVICE)

#         labels_batch = batch[
#             "labels"
#         ].to(DEVICE)

#         optimizer.zero_grad()

#         outputs = model(
#             input_ids=input_ids,
#             attention_mask=attention_mask
#         )

#         logits = outputs.logits

#         loss = criterion(
#             logits,
#             labels_batch
#         )

#         loss.backward()

#         optimizer.step()

#         total_train_loss += loss.item()

#         if (
#             batch_index + 1
#         ) % 100 == 0:

#             print(
#                 f"Epoch {epoch + 1}/{EPOCHS} "
#                 f"| Batch {batch_index + 1}/{len(train_loader)}"
#             )

#     train_loss = (
#         total_train_loss /
#         len(train_loader)
#     )

#     (
#         val_loss,
#         val_accuracy,
#         val_precision,
#         val_recall,
#         val_f1,
#         _,
#         _
#     ) = evaluate(
#         model,
#         val_loader
#     )

#     print("\n" + "-" * 70)

#     print(
#         f"Epoch {epoch + 1}/{EPOCHS}"
#     )

#     print(
#         f"Train Loss      : {train_loss:.4f}"
#     )

#     print(
#         f"Validation Loss : {val_loss:.4f}"
#     )

#     print(
#         f"Validation Acc  : {val_accuracy:.4f}"
#     )

#     print(
#         f"Validation Prec : {val_precision:.4f}"
#     )

#     print(
#         f"Validation Recall: {val_recall:.4f}"
#     )

#     print(
#         f"Validation F1   : {val_f1:.4f}"
#     )

#     print("-" * 70)

#     # --------------------------------------------------------
#     # SAVE BEST MODEL
#     # --------------------------------------------------------

#     if val_loss < best_val_loss:

#         best_val_loss = val_loss

#         epochs_without_improvement = 0

#         torch.save(
#             model.state_dict(),
#             best_model_path
#         )

#         print(
#             "Best model saved."
#         )

#     else:

#         epochs_without_improvement += 1

#         print(
#             "Validation loss did not improve."
#         )

#         if (
#             epochs_without_improvement
#             >= patience
#         ):

#             print(
#                 "Early stopping triggered."
#             )

#             break


# # ============================================================
# # LOAD BEST MODEL
# # ============================================================

# print("\n" + "=" * 70)
# print("LOADING BEST MODEL")
# print("=" * 70)

# model.load_state_dict(
#     torch.load(
#         best_model_path,
#         map_location=DEVICE
#     )
# )

# print(
#     "Best model loaded from:",
#     best_model_path
# )


# # ============================================================
# # FINAL TEST EVALUATION
# # ============================================================

# print("\n" + "=" * 70)
# print("FINAL TEST EVALUATION")
# print("=" * 70)

# (
#     test_loss,
#     test_accuracy,
#     test_precision,
#     test_recall,
#     test_f1,
#     actual,
#     predictions
# ) = evaluate(
#     model,
#     test_loader
# )


# print(
#     f"\nTest Loss : {test_loss:.4f}"
# )

# print(
#     f"Accuracy  : {test_accuracy:.4f}"
# )

# print(
#     f"Precision : {test_precision:.4f}"
# )

# print(
#     f"Recall    : {test_recall:.4f}"
# )

# print(
#     f"F1 Score  : {test_f1:.4f}"
# )


# # ============================================================
# # CLASSIFICATION REPORT
# # ============================================================

# print("\nClassification Report:")

# print(
#     classification_report(
#         actual,
#         predictions,
#         target_names=[
#             "Non-manipulative",
#             "Manipulative"
#         ],
#         zero_division=0
#     )
# )


# # ============================================================
# # CONFUSION MATRIX
# # ============================================================

# print("Confusion Matrix:")

# print(
#     confusion_matrix(
#         actual,
#         predictions
#     )
# )

# print("\nTraining complete.")


import random
import numpy as np
import pandas as pd
import torch

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

from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_PATH = "merged_scam_dataset.csv"

MODEL_NAME = "distilbert-base-uncased"

MAX_LENGTH = 256

BATCH_SIZE = 8

EPOCHS = 3

LEARNING_RATE = 2e-5

RANDOM_STATE = 42

# Early stopping based on validation F1
PATIENCE = 2

BEST_MODEL_PATH = "best_distilbert_baseline.pt"


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ============================================================
# REPRODUCIBILITY
# ============================================================

random.seed(RANDOM_STATE)
np.random.seed(RANDOM_STATE)
torch.manual_seed(RANDOM_STATE)

if torch.cuda.is_available():
    torch.cuda.manual_seed_all(RANDOM_STATE)


# ============================================================
# START
# ============================================================

print("=" * 70)
print("DISTILBERT BASELINE")
print("=" * 70)

print("\nDevice:", DEVICE)

if torch.cuda.is_available():

    print(
        "GPU:",
        torch.cuda.get_device_name(0)
    )

else:

    print(
        "GPU not available. Running on CPU."
    )


# ============================================================
# LOAD DATASET
# ============================================================

print("\n" + "=" * 70)
print("LOADING DATASET")
print("=" * 70)

df = pd.read_csv(
    DATASET_PATH
)

df = df.dropna(
    subset=["text", "label"]
).reset_index(drop=True)

df["text"] = df["text"].astype(str)
df["label"] = df["label"].astype(int)

print(
    "Dataset shape:",
    df.shape
)

print("\nLabel distribution:")
print(
    df["label"].value_counts()
)


texts = df["text"].to_numpy()
labels = df["label"].to_numpy()


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

print("\n" + "=" * 70)
print("TRAIN / TEST SPLIT")
print("=" * 70)

(
    text_train_full,
    text_test,
    y_train_full,
    y_test
) = train_test_split(
    texts,
    labels,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=labels
)


# ============================================================
# TRAIN / VALIDATION SPLIT
# ============================================================

(
    text_train,
    text_val,
    y_train,
    y_val
) = train_test_split(
    text_train_full,
    y_train_full,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y_train_full
)


print(
    "Training samples  :",
    len(text_train)
)

print(
    "Validation samples:",
    len(text_val)
)

print(
    "Testing samples   :",
    len(text_test)
)


# ============================================================
# LOAD TOKENIZER
# ============================================================

print("\n" + "=" * 70)
print("LOADING PRETRAINED DISTILBERT TOKENIZER")
print("=" * 70)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

print(
    "Tokenizer loaded successfully."
)


# ============================================================
# DATASET CLASS
# ============================================================

class ManipulationDataset(Dataset):

    def __init__(
        self,
        texts,
        labels,
        tokenizer,
        max_length
    ):

        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):

        return len(self.texts)

    def __getitem__(self, index):

        text = self.texts[index]
        label = self.labels[index]

        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt"
        )

        return {
            "input_ids": encoding[
                "input_ids"
            ].squeeze(0),

            "attention_mask": encoding[
                "attention_mask"
            ].squeeze(0),

            "labels": torch.tensor(
                label,
                dtype=torch.long
            )
        }


# ============================================================
# CREATE DATASETS
# ============================================================

train_dataset = ManipulationDataset(
    text_train,
    y_train,
    tokenizer,
    MAX_LENGTH
)

val_dataset = ManipulationDataset(
    text_val,
    y_val,
    tokenizer,
    MAX_LENGTH
)

test_dataset = ManipulationDataset(
    text_test,
    y_test,
    tokenizer,
    MAX_LENGTH
)


# ============================================================
# DATA LOADERS
# ============================================================

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


print("\nDataLoaders created.")

print(
    "Training batches  :",
    len(train_loader)
)

print(
    "Validation batches:",
    len(val_loader)
)

print(
    "Testing batches   :",
    len(test_loader)
)


# ============================================================
# CLASS WEIGHTS
# ============================================================

print("\n" + "=" * 70)
print("CLASS WEIGHTS")
print("=" * 70)

classes = np.unique(
    y_train
)

weights = compute_class_weight(
    class_weight="balanced",
    classes=classes,
    y=y_train
)

class_weights = torch.tensor(
    weights,
    dtype=torch.float
).to(DEVICE)


print(
    "Class weights:",
    {
        int(cls): float(weight)
        for cls, weight in zip(
            classes,
            weights
        )
    }
)


# ============================================================
# LOAD PRETRAINED DISTILBERT
# ============================================================

print("\n" + "=" * 70)
print("LOADING PRETRAINED DISTILBERT")
print("=" * 70)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=2
)

model.to(
    DEVICE
)

print(
    "DistilBERT loaded successfully."
)


# ============================================================
# MODEL PARAMETERS
# ============================================================

total_parameters = sum(
    p.numel()
    for p in model.parameters()
)

trainable_parameters = sum(
    p.numel()
    for p in model.parameters()
    if p.requires_grad
)

print(
    "\nTotal parameters:",
    f"{total_parameters:,}"
)

print(
    "Trainable parameters:",
    f"{trainable_parameters:,}"
)


# ============================================================
# OPTIMIZER
# ============================================================

optimizer = AdamW(
    model.parameters(),
    lr=LEARNING_RATE
)


# ============================================================
# LOSS FUNCTION
# ============================================================

criterion = torch.nn.CrossEntropyLoss(
    weight=class_weights
)


# ============================================================
# EVALUATION FUNCTION
# ============================================================

def evaluate(
    model,
    loader
):

    model.eval()

    total_loss = 0.0

    predictions = []
    actual_labels = []

    with torch.no_grad():

        for batch in loader:

            input_ids = batch[
                "input_ids"
            ].to(DEVICE)

            attention_mask = batch[
                "attention_mask"
            ].to(DEVICE)

            labels_batch = batch[
                "labels"
            ].to(DEVICE)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

            logits = outputs.logits

            loss = criterion(
                logits,
                labels_batch
            )

            total_loss += loss.item()

            preds = torch.argmax(
                logits,
                dim=1
            )

            predictions.extend(
                preds.cpu().numpy()
            )

            actual_labels.extend(
                labels_batch.cpu().numpy()
            )


    average_loss = (
        total_loss /
        len(loader)
    )

    accuracy = accuracy_score(
        actual_labels,
        predictions
    )

    precision = precision_score(
        actual_labels,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        actual_labels,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        actual_labels,
        predictions,
        zero_division=0
    )

    return (
        average_loss,
        accuracy,
        precision,
        recall,
        f1,
        actual_labels,
        predictions
    )


# ============================================================
# TRAINING
# ============================================================

print("\n" + "=" * 70)
print("TRAINING DISTILBERT")
print("=" * 70)

best_val_f1 = -1.0

epochs_without_improvement = 0


for epoch in range(
    EPOCHS
):

    model.train()

    total_train_loss = 0.0


    # --------------------------------------------------------
    # TRAINING LOOP
    # --------------------------------------------------------

    for batch_index, batch in enumerate(
        train_loader
    ):

        input_ids = batch[
            "input_ids"
        ].to(DEVICE)

        attention_mask = batch[
            "attention_mask"
        ].to(DEVICE)

        labels_batch = batch[
            "labels"
        ].to(DEVICE)


        optimizer.zero_grad()


        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        logits = outputs.logits


        loss = criterion(
            logits,
            labels_batch
        )


        loss.backward()

        optimizer.step()


        total_train_loss += loss.item()


        if (
            batch_index + 1
        ) % 100 == 0:

            print(
                f"Epoch {epoch + 1}/{EPOCHS} "
                f"| Batch {batch_index + 1}/{len(train_loader)}"
            )


    train_loss = (
        total_train_loss /
        len(train_loader)
    )


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

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


    print("\n" + "-" * 70)

    print(
        f"Epoch {epoch + 1}/{EPOCHS}"
    )

    print(
        f"Train Loss       : {train_loss:.4f}"
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
    # SAVE BEST MODEL BASED ON VALIDATION F1
    # --------------------------------------------------------

    if val_f1 > best_val_f1:

        best_val_f1 = val_f1

        epochs_without_improvement = 0


        torch.save(
            model.state_dict(),
            BEST_MODEL_PATH
        )


        print(
            f"New best validation F1: "
            f"{best_val_f1:.4f}"
        )

        print(
            "Best model saved."
        )


    else:

        epochs_without_improvement += 1

        print(
            "Validation F1 did not improve."
        )

        print(
            f"Patience: "
            f"{epochs_without_improvement}/{PATIENCE}"
        )


        if (
            epochs_without_improvement
            >= PATIENCE
        ):

            print(
                "\nEarly stopping triggered."
            )

            break


# ============================================================
# LOAD BEST MODEL
# ============================================================

print("\n" + "=" * 70)
print("LOADING BEST MODEL")
print("=" * 70)

model.load_state_dict(
    torch.load(
        BEST_MODEL_PATH,
        map_location=DEVICE
    )
)

print(
    "Best model loaded from:",
    BEST_MODEL_PATH
)

print(
    f"Best validation F1: "
    f"{best_val_f1:.4f}"
)


# ============================================================
# FINAL TEST EVALUATION
# ============================================================

print("\n" + "=" * 70)
print("FINAL TEST EVALUATION")
print("=" * 70)


(
    test_loss,
    test_accuracy,
    test_precision,
    test_recall,
    test_f1,
    actual,
    predictions
) = evaluate(
    model,
    test_loader
)


print(
    f"\nTest Loss : {test_loss:.4f}"
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

print(
    "\nClassification Report:"
)

print(
    classification_report(
        actual,
        predictions,
        target_names=[
            "Non-manipulative",
            "Manipulative"
        ],
        zero_division=0
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

print(
    "Confusion Matrix:"
)

print(
    confusion_matrix(
        actual,
        predictions
    )
)


# ============================================================
# COMPLETE
# ============================================================

print(
    "\nTraining complete."
)