import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input,
    Embedding,
    Bidirectional,
    LSTM,
    Dense,
    Dropout,
    Concatenate
)
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from tactic_features import extract_tactic_features


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_PATH = "merged_scam_dataset.csv"

MAX_LENGTH = 512
VOCAB_SIZE = 20000
EMBEDDING_DIM = 128

BATCH_SIZE = 32
EPOCHS = 15

RANDOM_STATE = 42


TACTICS = [
    "urgency_pressure",
    "fear_based_persuasion",
    "impersonation",
    "emotional_manipulation",
    "financial_extraction",
    "trust_engineering",
    "social_isolation",
    "coercion"
]


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("BiLSTM + TACTIC FEATURE FUSION")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv(DATASET_PATH)

df = df.dropna(
    subset=["text", "label"]
).reset_index(drop=True)

print("Dataset shape:", df.shape)

print("\nLabel distribution:")
print(df["label"].value_counts())


texts = df["text"].astype(str).to_numpy()
labels = df["label"].astype(int).to_numpy()


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

print("\n" + "=" * 70)
print("TRAIN / TEST SPLIT")
print("=" * 70)

(
    text_train,
    text_test,
    y_train,
    y_test
) = train_test_split(
    texts,
    labels,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=labels
)

print("Training samples:", len(text_train))
print("Testing samples :", len(text_test))


# ============================================================
# TOKENIZATION
# ============================================================

print("\n" + "=" * 70)
print("TEXT TOKENIZATION")
print("=" * 70)

tokenizer = Tokenizer(
    num_words=VOCAB_SIZE,
    oov_token="<OOV>"
)

tokenizer.fit_on_texts(text_train)

X_train_text = tokenizer.texts_to_sequences(
    text_train
)

X_test_text = tokenizer.texts_to_sequences(
    text_test
)

X_train_text = pad_sequences(
    X_train_text,
    maxlen=MAX_LENGTH,
    padding="post",
    truncating="post"
)

X_test_text = pad_sequences(
    X_test_text,
    maxlen=MAX_LENGTH,
    padding="post",
    truncating="post"
)

actual_vocab_size = min(
    VOCAB_SIZE,
    len(tokenizer.word_index) + 1
)

print("Vocabulary size:", actual_vocab_size)
print("Training text shape:", X_train_text.shape)
print("Testing text shape :", X_test_text.shape)


# ============================================================
# TACTIC FEATURES
# ============================================================

print("\n" + "=" * 70)
print("GENERATING TACTIC FEATURES")
print("=" * 70)


def generate_tactic_features(texts):

    features = []

    total = len(texts)

    for i, text in enumerate(texts):

        result = extract_tactic_features(text)

        features.append([
            result[tactic]
            for tactic in TACTICS
        ])

        if (i + 1) % 100 == 0 or i == total - 1:

            print(
                f"Processed {i + 1}/{total}"
            )

    return np.asarray(
        features,
        dtype=np.float32
    )


print("\nTraining tactic features:")

X_train_tactic = generate_tactic_features(
    text_train
)

print("\nTesting tactic features:")

X_test_tactic = generate_tactic_features(
    text_test
)

print("\nTraining tactic shape:")
print(X_train_tactic.shape)

print("Testing tactic shape:")
print(X_test_tactic.shape)


# ============================================================
# CLASS WEIGHTS
# ============================================================

print("\n" + "=" * 70)
print("CLASS WEIGHTS")
print("=" * 70)

classes = np.unique(y_train)

weights = compute_class_weight(
    class_weight="balanced",
    classes=classes,
    y=y_train
)

class_weights = {
    int(cls): float(weight)
    for cls, weight in zip(classes, weights)
}

print("Class weights:")
print(class_weights)


# ============================================================
# TEXT BRANCH
# ============================================================

text_input = Input(
    shape=(MAX_LENGTH,),
    name="text_input"
)

text_embedding = Embedding(
    input_dim=actual_vocab_size,
    output_dim=EMBEDDING_DIM,
    name="text_embedding"
)(text_input)

text_branch = Bidirectional(
    LSTM(
        128,
        return_sequences=True
    ),
    name="bilstm_128"
)(text_embedding)

text_branch = Dropout(
    0.4
)(text_branch)

text_branch = Bidirectional(
    LSTM(
        64
    ),
    name="bilstm_64"
)(text_branch)

text_branch = Dropout(
    0.4
)(text_branch)


# ============================================================
# TACTIC BRANCH
# ============================================================

tactic_input = Input(
    shape=(len(TACTICS),),
    name="tactic_input"
)

tactic_branch = Dense(
    16,
    activation="relu",
    name="tactic_dense"
)(tactic_input)

tactic_branch = Dropout(
    0.2
)(tactic_branch)


# ============================================================
# FEATURE FUSION
# ============================================================

combined = Concatenate(
    name="feature_fusion"
)([
    text_branch,
    tactic_branch
])


# ============================================================
# CLASSIFICATION HEAD
# ============================================================

combined = Dense(
    32,
    activation="relu"
)(combined)

combined = Dropout(
    0.3
)(combined)

output = Dense(
    1,
    activation="sigmoid",
    name="output"
)(combined)


# ============================================================
# MODEL
# ============================================================

model = Model(
    inputs=[
        text_input,
        tactic_input
    ],
    outputs=output
)


# ============================================================
# COMPILE
# ============================================================

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=[
        "accuracy"
    ]
)


# ============================================================
# MODEL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("MODEL SUMMARY")
print("=" * 70)

model.summary()


# ============================================================
# TRAIN
# ============================================================

print("\n" + "=" * 70)
print("TRAINING")
print("=" * 70)

from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

callbacks = [
    EarlyStopping(
        monitor="val_loss",
        patience=2,
        restore_best_weights=True
    ),
    ModelCheckpoint(
        "best_bilstm_tactic.keras",
        monitor="val_loss",
        save_best_only=True
    )
]
history = model.fit(
    {
        "text_input": X_train_text,
        "tactic_input": X_train_tactic
    },
    y_train,
    validation_split=0.20,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    class_weight=class_weights,
    verbose=1,
    callbacks=callbacks
)


# ============================================================
# PREDICTION
# ============================================================

print("\n" + "=" * 70)
print("EVALUATION")
print("=" * 70)

probabilities = model.predict(
    {
        "text_input": X_test_text,
        "tactic_input": X_test_tactic
    },
    batch_size=BATCH_SIZE
).ravel()

y_pred = (
    probabilities >= 0.5
).astype(int)


# ============================================================
# METRICS
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)


print("\nBiLSTM + Tactic Features")

print(
    f"Accuracy : {accuracy:.4f}"
)

print(
    f"Precision: {precision:.4f}"
)

print(
    f"Recall   : {recall:.4f}"
)

print(
    f"F1 Score : {f1:.4f}"
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
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

print("Confusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)