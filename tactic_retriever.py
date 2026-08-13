from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from semantic_groups import SEMANTIC_GROUPS


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Initial threshold.
# We will NOT assume this is optimal.
# We will tune it using evaluation data later.
TACTIC_THRESHOLD = 0.40


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Model loaded successfully!")
print("Embedding dimension:", model.get_embedding_dimension())


# ============================================================
# PREPARE TACTIC VOCABULARY
# ============================================================

print("\nPreparing tactic vocabulary...")

group_embeddings = {}

for tactic, groups in SEMANTIC_GROUPS.items():

    group_embeddings[tactic] = {}

    for group_name, terms in groups.items():

        embeddings = model.encode(
            terms,
            normalize_embeddings=True
        )

        group_embeddings[tactic][group_name] = {
            "terms": terms,
            "embeddings": embeddings
        }


print("Tactic vocabulary prepared.")


# ============================================================
# TACTIC RETRIEVAL
# ============================================================

def detect_tactics(text,threshold=TACTIC_THRESHOLD):

    """
    Detect tactics in a conversation using semantic similarity.

    Returns:
        List of detected tactics with:
        - tactic
        - score
        - semantic group
        - matched term
    """

    text_embedding = model.encode(
        [text],
        normalize_embeddings=True
    )

    results = []

    for tactic, groups in group_embeddings.items():

        best_score = -1
        best_group = None
        best_term = None

        for group_name, data in groups.items():

            similarities = cosine_similarity(
                text_embedding,
                data["embeddings"]
            )[0]

            best_index = similarities.argmax()
            score = float(similarities[best_index])

            if score > best_score:

                best_score = score
                best_group = group_name
                best_term = data["terms"][best_index]

        if best_score >= threshold:

            results.append({
                "tactic": tactic,
                "score": best_score,
                "group": best_group,
                "matched_term": best_term
            })

    # Highest confidence first
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results


# ============================================================
# TEST CONVERSATIONS
# ============================================================

# test_conversations = [

#     "Your account will be blocked in 10 minutes. Send me the OTP immediately.",

#     "I am calling from your bank's fraud department. You need to verify your account.",

#     "Don't tell anyone about this. Keep this between us.",

#     "You have no choice. Do exactly what I say.",

#     "After everything I have done for you, you owe me this.",

#     "Hello, how are you? I hope you are having a good day."
# ]


# # ============================================================
# # RUN TESTS
# # ============================================================

# for conversation in test_conversations:

#     print("\n" + "=" * 80)

#     print("Conversation:")
#     print(conversation)

#     print("\nDetected tactics:")

#     results = detect_tactics(conversation)

#     if not results: 

#         print("None")

#     else:

#         for result in results:

#             print(
#                 f"- {result['tactic']}"
#                 f" | score={result['score']:.4f}"
#                 f" | group={result['group']}"
#                 f" | matched='{result['matched_term']}'"
#             )