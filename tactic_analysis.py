import pandas as pd
import numpy as np

from tactic_features import extract_tactic_features


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


print("=" * 70)
print("TACTIC FEATURE ANALYSIS")
print("=" * 70)

df = pd.read_csv(DATASET_PATH)

print("\nDataset:", df.shape)


# ============================================================
# GENERATE FEATURES
# ============================================================

features = []

for i, text in enumerate(df["text"]):

    result = extract_tactic_features(text)

    features.append([
        result[tactic]
        for tactic in TACTICS
    ])

    if (i + 1) % 500 == 0:
        print(f"Processed {i + 1}/{len(df)}")


feature_df = pd.DataFrame(
    features,
    columns=TACTICS
)

feature_df["label"] = df["label"].values


# ============================================================
# MEAN SCORES BY CLASS
# ============================================================

print("\n" + "=" * 70)
print("AVERAGE TACTIC SCORE BY CLASS")
print("=" * 70)

mean_scores = feature_df.groupby("label")[TACTICS].mean()

print(
    mean_scores.round(4).to_string()
)


# ============================================================
# DIFFERENCE
# ============================================================

print("\n" + "=" * 70)
print("CLASS DIFFERENCE")
print("=" * 70)

difference = (
    mean_scores.loc[1]
    - mean_scores.loc[0]
)

difference_df = pd.DataFrame({
    "tactic": TACTICS,
    "mean_non_manipulative": mean_scores.loc[0].values,
    "mean_manipulative": mean_scores.loc[1].values,
    "difference": difference.values
})

difference_df["absolute_difference"] = (
    difference_df["difference"].abs()
)

difference_df = difference_df.sort_values(
    "absolute_difference",
    ascending=False
)

print(
    difference_df.round(4).to_string(index=False)
)


# ============================================================
# STANDARD DEVIATION
# ============================================================

print("\n" + "=" * 70)
print("STANDARD DEVIATION BY CLASS")
print("=" * 70)

std_scores = feature_df.groupby("label")[TACTICS].std()

print(
    std_scores.round(4).to_string()
)