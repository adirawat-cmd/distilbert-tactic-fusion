# from sentence_transformers import SentenceTransformer

# print("Loading embedding model...")

# model = SentenceTransformer("all-MiniLM-L6-v2")

# print("Model loaded successfully!")

# print("Embedding dimension:", model.get_sentence_embedding_dimension())

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --------------------------------------------------
# 1. Load pretrained embedding model
# --------------------------------------------------

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully!")
print(
    "Embedding dimension:",
    model.get_embedding_dimension()
)


# --------------------------------------------------
# 2. Our initial urgency marker vocabulary
# --------------------------------------------------

URGENCY_MARKERS = [
    "immediately",
    "right now",
    "right away",
    "at once",
    "now",

    "hurry",
    "hurry up",
    "act fast",
    "act quickly",
    "don't wait",
    "do it quickly",

    "deadline",
    "within",
    "before",
    "expires",
    "expires today",
    "last chance",
    "final warning",

    "within 5 minutes",
    "within 10 minutes",
    "within an hour",
    "today only",
    "before midnight",
    "before it's too late",

    "urgent",
    "critical",
    "immediate",
    "pressing",
    "time-sensitive"
]


# --------------------------------------------------
# 3. Convert markers into embeddings
# --------------------------------------------------

print("\nGenerating embeddings...")

embeddings = model.encode(
    URGENCY_MARKERS,
    normalize_embeddings=True
)

print("Embedding shape:", embeddings.shape)


# --------------------------------------------------
# 4. Calculate cosine similarity
# --------------------------------------------------

similarity_matrix = cosine_similarity(embeddings)


# --------------------------------------------------
# 5. Show most similar terms for every marker
# --------------------------------------------------

print("\n" + "=" * 70)
print("SEMANTIC SIMILARITY RESULTS")
print("=" * 70)

for i, marker in enumerate(URGENCY_MARKERS):

    similarities = []

    for j, other_marker in enumerate(URGENCY_MARKERS):

        if i == j:
            continue

        similarities.append(
            (other_marker, similarity_matrix[i][j])
        )

    # Sort from highest similarity to lowest
    similarities.sort(
        key=lambda x: x[1],
        reverse=True
    )

    print("\n" + "-" * 70)
    print(f"Seed: {marker}")

    print("Most similar terms:")

    for term, score in similarities[:5]:
        print(f"  {term:<30} {score:.4f}")