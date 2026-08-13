from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from tactic_dictionary import TACTICS
from tactic_candidates import CANDIDATES


# ============================================================
# 1. Load embedding model
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

    candidates = CANDIDATES[tactic_id]

    print("Seeds:", len(seeds))
    print("Candidates:", len(candidates))


    # --------------------------------------------------------
    # Generate embeddings
    # --------------------------------------------------------

    seed_embeddings = model.encode(
        seeds,
        normalize_embeddings=True
    )

    candidate_embeddings = model.encode(
        candidates,
        normalize_embeddings=True
    )


    # --------------------------------------------------------
    # Calculate candidate → seed similarity
    # --------------------------------------------------------

    similarity_matrix = cosine_similarity(
        candidate_embeddings,
        seed_embeddings
    )


    # --------------------------------------------------------
    # Find best seed for every candidate
    # --------------------------------------------------------

    results = []

    for i, candidate in enumerate(candidates):

        best_seed_index = similarity_matrix[i].argmax()

        best_seed = seeds[best_seed_index]

        best_score = similarity_matrix[i][best_seed_index]

        results.append(
            (
                candidate,
                best_seed,
                best_score
            )
        )


    # --------------------------------------------------------
    # Sort highest → lowest
    # --------------------------------------------------------

    results.sort(
        key=lambda x: x[2],
        reverse=True
    )


    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    print("\nCandidate ranking:")

    for candidate, seed, score in results:

        print(
            f"{candidate:<40} "
            f"{score:.4f} "
            f"→ {seed}"
        )