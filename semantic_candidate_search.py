from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# 1. Load pretrained embedding model
# --------------------------------------------------

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully!")


# --------------------------------------------------
# 2. Seed urgency concepts
# --------------------------------------------------

SEEDS = [
    "urgent",
    "immediately",
    "right now",
    "act fast",
    "hurry",
    "deadline",
    "last chance",
    "time-sensitive"
]


# --------------------------------------------------
# 3. Candidate expressions
# --------------------------------------------------

CANDIDATES = [
    # Strong urgency candidates
    "don't delay",
    "without delay",
    "waste no time",
    "take action now",
    "respond immediately",
    "respond promptly",
    "act without delay",
    "do not hesitate",
    "no time to waste",
    "time is running out",
    "running out of time",
    "limited time",
    "short window",
    "limited window",
    "immediate action",
    "prompt action",
    "quick response",
    "fast response",
    "respond now",
    "contact us now",

    # Ambiguous candidates
    "soon",
    "promptly",
    "rapidly",
    "quickly",
    "as soon as possible",
    "at your earliest convenience",
    "priority",
    "high priority",
    "important",
    "essential"
]


# --------------------------------------------------
# 4. Generate embeddings
# --------------------------------------------------

print("\nGenerating seed embeddings...")

seed_embeddings = model.encode(
    SEEDS,
    normalize_embeddings=True
)

print("Generating candidate embeddings...")

candidate_embeddings = model.encode(
    CANDIDATES,
    normalize_embeddings=True
)


# --------------------------------------------------
# 5. Calculate similarity
# --------------------------------------------------

similarity_matrix = cosine_similarity(
    candidate_embeddings,
    seed_embeddings
)


# --------------------------------------------------
# 6. Find strongest seed relationship
# --------------------------------------------------

print("\n" + "=" * 75)
print("CANDIDATE URGENCY SEMANTIC SEARCH")
print("=" * 75)

results = []

for i, candidate in enumerate(CANDIDATES):

    # Find the seed with highest similarity
    best_seed_index = similarity_matrix[i].argmax()

    best_seed = SEEDS[best_seed_index]

    best_score = similarity_matrix[i][best_seed_index]

    results.append(
        (
            candidate,
            best_seed,
            best_score
        )
    )


# Sort candidates by similarity
results.sort(
    key=lambda x: x[2],
    reverse=True
)


# --------------------------------------------------
# 7. Display results
# --------------------------------------------------

for candidate, seed, score in results:

    print(
        f"{candidate:<35} "
        f"{score:.4f} "
        f"→ {seed}"
    )