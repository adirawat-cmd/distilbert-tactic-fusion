import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from tactic_features import extract_tactic_features


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_PATH = "merged_scam_dataset.csv"

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
# LOAD DATASET
# ============================================================

print("=" * 70)
print("TACTIC-ONLY BASELINE")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv(DATASET_PATH)

print("Dataset shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nLabel distribution:")
print(df["label"].value_counts())


# ============================================================
# GENERATE TACTIC FEATURES
# ============================================================

print("\n" + "=" * 70)
print("GENERATING TACTIC FEATURES")
print("=" * 70)

feature_rows = []

total = len(df)

for i, text in enumerate(df["text"]):

    features = extract_tactic_features(text)

    row = [
        features[tactic]
        for tactic in TACTICS
    ]

    feature_rows.append(row)

    if (i + 1) % 100 == 0 or i == total - 1:
        print(
            f"Processed {i + 1}/{total} samples"
        )


X = np.array(feature_rows)
y = df["label"].values


print("\nFeature matrix shape:", X.shape)
print("Expected shape:", (len(df), len(TACTICS)))


# ============================================================
# DISPLAY SAMPLE FEATURES
# ============================================================

feature_df = pd.DataFrame(
    X,
    columns=TACTICS
)

print("\nFirst 5 feature vectors:")

print(
    feature_df.head().round(4)
)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

print("\n" + "=" * 70)
print("TRAIN / TEST SPLIT")
print("=" * 70)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples :", len(X_test))


# ============================================================
# TRAIN LOGISTIC REGRESSION
# ============================================================

print("\n" + "=" * 70)
print("TRAINING TACTIC-ONLY CLASSIFIER")
print("=" * 70)

classifier = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)

classifier.fit(
    X_train,
    y_train
)

print("Training complete.")


# ============================================================
# PREDICTION
# ============================================================

y_pred = classifier.predict(X_test)


# ============================================================
# EVALUATION
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


print("\n" + "=" * 70)
print("TACTIC-ONLY RESULTS")
print("=" * 70)

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")


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


# ============================================================
# TACTIC IMPORTANCE
# ============================================================

print("\n" + "=" * 70)
print("TACTIC FEATURE IMPORTANCE")
print("=" * 70)

coefficients = classifier.coef_[0]

importance_df = pd.DataFrame({
    "tactic": TACTICS,
    "coefficient": coefficients,
    "absolute_importance": np.abs(coefficients)
})

importance_df = importance_df.sort_values(
    "absolute_importance",
    ascending=False
)

print(
    importance_df.to_string(
        index=False
    )
)