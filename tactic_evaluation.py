# from tactic_retriever import detect_tactics
# EVALUATION_DATA = [

#     # ============================================================
#     # URGENCY PRESSURE
#     # ============================================================

#     {
#         "text": "Act immediately or your account will be closed.",
#         "expected_tactics": ["urgency_pressure"]
#     },

#     {
#         "text": "You have only five minutes to complete the payment.",
#         "expected_tactics": ["urgency_pressure"]
#     },

#     {
#         "text": "Please respond whenever convenient.",
#         "expected_tactics": []
#     },


#     # ============================================================
#     # FEAR-BASED PERSUASION
#     # ============================================================

#     {
#         "text": "Your account will be suspended if you do not comply.",
#         "expected_tactics": ["fear_based_persuasion"]
#     },

#     {
#         "text": "You will lose all your money if you do not act.",
#         "expected_tactics": ["fear_based_persuasion"]
#     },

#     {
#         "text": "Your account is working normally.",
#         "expected_tactics": []
#     },


#     # ============================================================
#     # IMPERSONATION
#     # ============================================================

#     {
#         "text": "I am calling from your bank's fraud department.",
#         "expected_tactics": ["impersonation"]
#     },

#     {
#         "text": "I am a government official contacting you about your account.",
#         "expected_tactics": ["impersonation"]
#     },

#     {
#         "text": "I spoke with a bank representative yesterday.",
#         "expected_tactics": []
#     },


#     # ============================================================
#     # EMOTIONAL MANIPULATION
#     # ============================================================

#     {
#         "text": "After everything I have done for you, you owe me this.",
#         "expected_tactics": ["emotional_manipulation"]
#     },

#     {
#         "text": "If you really loved me, you would do this.",
#         "expected_tactics": ["emotional_manipulation"]
#     },

#     {
#         "text": "Thank you for helping me today.",
#         "expected_tactics": []
#     },


#     # ============================================================
#     # FINANCIAL EXTRACTION
#     # ============================================================

#     {
#         "text": "Send me your OTP to verify your account.",
#         "expected_tactics": ["financial_extraction"]
#     },

#     {
#         "text": "Please transfer the money to this account.",
#         "expected_tactics": ["financial_extraction"]
#     },

#     {
#         "text": "I checked my bank account this morning.",
#         "expected_tactics": []
#     },


#     # ============================================================
#     # TRUST ENGINEERING
#     # ============================================================

#     {
#         "text": "You can trust me. I have helped customers for years.",
#         "expected_tactics": ["trust_engineering"]
#     },

#     {
#         "text": "You are in good hands. I will take care of everything.",
#         "expected_tactics": ["trust_engineering"]
#     },

#     {
#         "text": "I don't know anything about your situation.",
#         "expected_tactics": []
#     },


#     # ============================================================
#     # SOCIAL ISOLATION
#     # ============================================================

#     {
#         "text": "Don't tell anyone about this.",
#         "expected_tactics": ["social_isolation"]
#     },

#     {
#         "text": "Do not contact your bank about this matter.",
#         "expected_tactics": ["social_isolation"]
#     },

#     {
#         "text": "Please tell your family about the situation.",
#         "expected_tactics": []
#     },


#     # ============================================================
#     # COERCION
#     # ============================================================

#     {
#         "text": "You have no choice. Do exactly what I say.",
#         "expected_tactics": ["coercion"]
#     },

#     {
#         "text": "You must comply with my instructions.",
#         "expected_tactics": ["coercion"]
#     },

#     {
#         "text": "You are free to decide what you want to do.",
#         "expected_tactics": []
#     }
# ]

from tactic_retriever import detect_tactics


EVALUATION_DATA = [

    # ============================================================
    # URGENCY PRESSURE
    # ============================================================

    {
        "text": "Act immediately or your account will be closed.",
        "expected_tactics": ["urgency_pressure"]
    },

    {
        "text": "You have only five minutes to complete the payment.",
        "expected_tactics": ["urgency_pressure"]
    },

    {
        "text": "Please respond whenever convenient.",
        "expected_tactics": []
    },


    # ============================================================
    # FEAR-BASED PERSUASION
    # ============================================================

    {
        "text": "Your account will be suspended if you do not comply.",
        "expected_tactics": ["fear_based_persuasion"]
    },

    {
        "text": "You will lose all your money if you do not act.",
        "expected_tactics": ["fear_based_persuasion"]
    },

    {
        "text": "Your account is working normally.",
        "expected_tactics": []
    },


    # ============================================================
    # IMPERSONATION
    # ============================================================

    {
        "text": "I am calling from your bank's fraud department.",
        "expected_tactics": ["impersonation"]
    },

    {
        "text": "I am a government official contacting you about your account.",
        "expected_tactics": ["impersonation"]
    },

    {
        "text": "I spoke with a bank representative yesterday.",
        "expected_tactics": []
    },


    # ============================================================
    # EMOTIONAL MANIPULATION
    # ============================================================

    {
        "text": "After everything I have done for you, you owe me this.",
        "expected_tactics": ["emotional_manipulation"]
    },

    {
        "text": "If you really loved me, you would do this.",
        "expected_tactics": ["emotional_manipulation"]
    },

    {
        "text": "Thank you for helping me today.",
        "expected_tactics": []
    },


    # ============================================================
    # FINANCIAL EXTRACTION
    # ============================================================

    {
        "text": "Send me your OTP to verify your account.",
        "expected_tactics": ["financial_extraction"]
    },

    {
        "text": "Please transfer the money to this account.",
        "expected_tactics": ["financial_extraction"]
    },

    {
        "text": "I checked my bank account this morning.",
        "expected_tactics": []
    },


    # ============================================================
    # TRUST ENGINEERING
    # ============================================================

    {
        "text": "You can trust me. I have helped customers for years.",
        "expected_tactics": ["trust_engineering"]
    },

    {
        "text": "You are in good hands. I will take care of everything.",
        "expected_tactics": ["trust_engineering"]
    },

    {
        "text": "I don't know anything about your situation.",
        "expected_tactics": []
    },


    # ============================================================
    # SOCIAL ISOLATION
    # ============================================================

    {
        "text": "Don't tell anyone about this.",
        "expected_tactics": ["social_isolation"]
    },

    {
        "text": "Do not contact your bank about this matter.",
        "expected_tactics": ["social_isolation"]
    },

    {
        "text": "Please tell your family about the situation.",
        "expected_tactics": []
    },


    # ============================================================
    # COERCION
    # ============================================================

    {
        "text": "You have no choice. Do exactly what I say.",
        "expected_tactics": ["coercion"]
    },

    {
        "text": "You must comply with my instructions.",
        "expected_tactics": ["coercion"]
    },

    {
        "text": "You are free to decide what you want to do.",
        "expected_tactics": []
    }
]


# ============================================================
# HELPER FUNCTION
# ============================================================

def evaluate_threshold(threshold):

    """
    Evaluate the tactic retriever at a particular
    similarity threshold.

    Returns precision, recall and F1.
    """

    true_positive = 0
    false_positive = 0
    false_negative = 0

    for sample in EVALUATION_DATA:

        text = sample["text"]
        expected = set(sample["expected_tactics"])

        results = detect_tactics(text, threshold=threshold)

        # detect_tactics currently uses the threshold
        # inside tactic_retriever.py.
        predicted = set(
            result["tactic"]
            for result in results
        )

        # Only count tactics relevant to this evaluation set.
        true_positive += len(predicted & expected)

        false_positive += len(predicted - expected)

        false_negative += len(expected - predicted)

    precision = (
        true_positive /
        (true_positive + false_positive)
        if (true_positive + false_positive) > 0
        else 0
    )

    recall = (
        true_positive /
        (true_positive + false_negative)
        if (true_positive + false_negative) > 0
        else 0
    )

    f1 = (
        2 * precision * recall /
        (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    return precision, recall, f1


# ============================================================
# RUN BASIC EVALUATION
# ============================================================

# if __name__ == "__main__":

#     print("=" * 80)
#     print("TACTIC RETRIEVAL EVALUATION")
#     print("=" * 80)

#     print("\nNumber of evaluation samples:", len(EVALUATION_DATA))

#     print("\nCurrent threshold:", 0.40)

#     precision, recall, f1 = evaluate_threshold(0.40)

#     print("\nResults")
#     print("-" * 40)

#     print(f"Precision: {precision:.4f}")
#     print(f"Recall:    {recall:.4f}")
#     print(f"F1 Score:  {f1:.4f}")

if __name__ == "__main__":

    print("=" * 80)
    print("TACTIC RETRIEVAL THRESHOLD EVALUATION")
    print("=" * 80)

    print("\nEvaluation samples:", len(EVALUATION_DATA))

    thresholds = [
        0.30,
        0.35,
        0.40,
        0.45,
        0.50,
        0.55,
        0.60,
        0.65,
        0.70
    ]

    print("\n")
    print(
        f"{'Threshold':<12}"
        f"{'Precision':<12}"
        f"{'Recall':<12}"
        f"{'F1':<12}"
    )

    print("-" * 48)

    for threshold in thresholds:

        precision, recall, f1 = evaluate_threshold(
            threshold
        )

        print(
            f"{threshold:<12.2f}"
            f"{precision:<12.4f}"
            f"{recall:<12.4f}"
            f"{f1:<12.4f}"
        )