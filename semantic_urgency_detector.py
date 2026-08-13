from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# 1. Load model
# --------------------------------------------------

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully!")


# --------------------------------------------------
# 2. Urgency seed concepts
# --------------------------------------------------

URGENCY_SEEDS = [
    "urgent",
    "immediate action",
    "act immediately",
    "act right now",
    "hurry",
    "time pressure",
    "deadline",
    "limited time",
    "time-sensitive",
    "last chance",
    "final warning",
    "running out of time"
]


# --------------------------------------------------
# 3. Test sentences
# --------------------------------------------------

TEST_SENTENCES = [
    "Your account will be closed unless you act immediately.",

    "You have only 10 minutes to complete the payment.",

    "Please respond promptly so that we can process your request.",

    "I hope you have a good day. Please contact me whenever convenient.",

    "This is your final warning. Your account expires today.",

    "There is no need to hurry. You can complete this whenever you want."
]


# --------------------------------------------------
# 4. Generate embeddings
# --------------------------------------------------

print("\nGenerating seed embeddings...")

seed_embeddings = model.encode(
    URGENCY_SEEDS,
    normalize_embeddings=True
)


print("Generating sentence embeddings...")

sentence_embeddings = model.encode(
    TEST_SENTENCES,
    normalize_embeddings=True
)


# --------------------------------------------------
# 5. Calculate similarity
# --------------------------------------------------

similarity_matrix = cosine_similarity(
    sentence_embeddings,
    seed_embeddings
)


# --------------------------------------------------
# 6. Display best matching urgency concept
# --------------------------------------------------

print("\n" + "=" * 75)
print("SEMANTIC URGENCY DETECTION")
print("=" * 75)


for i, sentence in enumerate(TEST_SENTENCES):

    best_index = similarity_matrix[i].argmax()

    best_seed = URGENCY_SEEDS[best_index]

    best_score = similarity_matrix[i][best_index]

    print("\nSentence:")
    print(sentence)

    print("\nMost similar urgency concept:")
    print(best_seed)

    print(f"Similarity score: {best_score:.4f}")