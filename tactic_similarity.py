from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from tactic_dictionary import TACTICS


# ============================================================
# 1. Load pretrained embedding model
# ============================================================

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully!")


# ============================================================
# 2. Process each tactic
# ============================================================

for tactic_id, tactic in TACTICS.items():

    print("\n" + "=" * 80)

    print("TACTIC:", tactic["name"])

    print("=" * 80)

    seeds = tactic["seed_terms"]

    print("Number of seeds:", len(seeds))

    # Generate embeddings
    embeddings = model.encode(
        seeds,
        normalize_embeddings=True
    )

    # Calculate similarity
    similarity_matrix = cosine_similarity(
        embeddings
    )

    print("\nMost similar seed pairs:")

    pairs = []

    for i in range(len(seeds)):

        for j in range(i + 1, len(seeds)):

            score = similarity_matrix[i][j]

            pairs.append(
                (
                    seeds[i],
                    seeds[j],
                    score
                )
            )

    # Highest similarity first
    pairs.sort(
        key=lambda x: x[2],
        reverse=True
    )

    # Display top 5
    for seed1, seed2, score in pairs[:5]:

        print(
            f"{seed1:<40} ↔ "
            f"{seed2:<40} "
            f"{score:.4f}"
        )