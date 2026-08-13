from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# 1. Load pretrained embedding model
# ============================================================

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully!")


# ============================================================
# 2. Define urgency seed concepts
# ============================================================

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


# ============================================================
# 3. Evaluation dataset
# ============================================================

evaluation_data = [

    # --------------------------------------------------------
    # A. CLEAR URGENCY
    # --------------------------------------------------------

    {
        "text": "Act immediately.",
        "category": "clear_urgency"
    },

    {
        "text": "You have only five minutes.",
        "category": "clear_urgency"
    },

    {
        "text": "Do this right now.",
        "category": "clear_urgency"
    },

    {
        "text": "Your account expires today.",
        "category": "clear_urgency"
    },

    {
        "text": "You need to respond without delay.",
        "category": "clear_urgency"
    },


    # --------------------------------------------------------
    # B. NO URGENCY
    # --------------------------------------------------------

    {
        "text": "You can complete this whenever convenient.",
        "category": "no_urgency"
    },

    {
        "text": "There is no rush.",
        "category": "no_urgency"
    },

    {
        "text": "Take your time.",
        "category": "no_urgency"
    },

    {
        "text": "You can respond whenever you are ready.",
        "category": "no_urgency"
    },

    {
        "text": "There is no need to hurry.",
        "category": "no_urgency"
    },


    # --------------------------------------------------------
    # C. LEGITIMATE URGENCY
    # --------------------------------------------------------

    {
        "text": "Please arrive at the airport two hours before your flight.",
        "category": "legitimate_urgency"
    },

    {
        "text": "This medical situation requires immediate attention.",
        "category": "legitimate_urgency"
    },

    {
        "text": "Please submit the application before the deadline.",
        "category": "legitimate_urgency"
    },

    {
        "text": "The meeting starts in ten minutes.",
        "category": "legitimate_urgency"
    },

    {
        "text": "Please respond promptly so we can process your request.",
        "category": "legitimate_urgency"
    },


    # --------------------------------------------------------
    # D. MANIPULATIVE URGENCY
    # --------------------------------------------------------

    {
        "text": "Send the OTP within five minutes or your account will be blocked.",
        "category": "manipulative_urgency"
    },

    {
        "text": "Act now or you will lose your money.",
        "category": "manipulative_urgency"
    },

    {
        "text": "You must make the payment immediately or your account will be suspended.",
        "category": "manipulative_urgency"
    },

    {
        "text": "This is your final warning. Transfer the money now.",
        "category": "manipulative_urgency"
    },

    {
        "text": "You have ten minutes to verify your account before it is permanently closed.",
        "category": "manipulative_urgency"
    }
]


# ============================================================
# 4. Generate embeddings
# ============================================================

print("\nGenerating seed embeddings...")

seed_embeddings = model.encode(
    URGENCY_SEEDS,
    normalize_embeddings=True
)

print("Generating evaluation embeddings...")

texts = [
    item["text"]
    for item in evaluation_data
]

text_embeddings = model.encode(
    texts,
    normalize_embeddings=True
)


# ============================================================
# 5. Calculate similarities
# ============================================================

similarity_matrix = cosine_similarity(
    text_embeddings,
    seed_embeddings
)


# ============================================================
# 6. Display results
# ============================================================

print("\n")
print("=" * 80)
print("SEMANTIC URGENCY EVALUATION")
print("=" * 80)


for i, item in enumerate(evaluation_data):

    best_index = similarity_matrix[i].argmax()

    best_seed = URGENCY_SEEDS[best_index]

    best_score = similarity_matrix[i][best_index]

    print("\n" + "-" * 80)

    print("Category:")
    print(item["category"])

    print("\nText:")
    print(item["text"])

    print("\nMost similar urgency concept:")
    print(best_seed)

    print(f"Similarity score: {best_score:.4f}")