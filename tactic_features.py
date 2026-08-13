from tactic_retriever import group_embeddings
from tactic_retriever import model
from sklearn.metrics.pairwise import cosine_similarity


def extract_tactic_features(text):

    """
    Convert an input conversation into one semantic score
    for each tactic.

    Returns:
        Dictionary:
        {
            "urgency_pressure": score,
            "fear_based_persuasion": score,
            ...
        }
    """

    text_embedding = model.encode(
        [text],
        normalize_embeddings=True
    )

    tactic_features = {}

    for tactic, groups in group_embeddings.items():

        group_scores = []

        for group_name, data in groups.items():

            similarities = cosine_similarity(
                text_embedding,
                data["embeddings"]
            )[0]

            best_score = float(similarities.max())

            group_scores.append(best_score)

        # Strongest semantic evidence for this tactic
        tactic_score = max(group_scores)

        tactic_features[tactic] = tactic_score

    return tactic_features


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_conversations = [

        "Your account will be blocked in 10 minutes. Send me the OTP immediately.",

        "I am calling from your bank's fraud department. You need to verify your account.",

        "Don't tell anyone about this. Keep this between us.",

        "You have no choice. Do exactly what I say.",

        "After everything I have done for you, you owe me this.",

        "Hello, how are you? I hope you are having a good day."
    ]

    for text in test_conversations:

        print("\n" + "=" * 80)

        print("Conversation:")
        print(text)

        print("\nTactic feature scores:")

        features = extract_tactic_features(text)

        # Highest score first
        ranked = sorted(
            features.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for tactic, score in ranked:

            print(
                f"{tactic:<30} {score:.4f}"
            )