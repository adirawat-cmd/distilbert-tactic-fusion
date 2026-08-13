TACTICS = {

    "urgency_pressure": {

        "name": "Urgency Pressure",

        "definition": (
            "Creating time pressure or a sense of immediate action "
            "to discourage the target from thinking or verifying information."
        ),

        "seed_terms": [
            "urgent",
            "immediately",
            "right now",
            "right away",
            "act now",
            "act fast",
            "hurry",
            "deadline",
            "last chance",
            "final warning",
            "limited time",
            "time-sensitive",
            "expires today",
            "within minutes"
        ]
    },


    "fear_based_persuasion": {

        "name": "Fear-Based Persuasion",

        "definition": (
            "Using threats, danger, negative consequences, or fear "
            "to influence the target's behavior."
        ),

        "seed_terms": [
            "you will be blocked",
            "your account will be suspended",
            "you will lose your money",
            "legal action",
            "you will be arrested",
            "danger",
            "warning",
            "threat",
            "security threat",
            "negative consequences",
            "your account is at risk",
            "you could lose everything"
        ]
    },


    "impersonation": {

        "name": "Impersonation",

        "definition": (
            "Pretending to be a trusted person, organization, authority, "
            "or service in order to gain credibility."
        ),

        "seed_terms": [
            "I am calling from your bank",
            "I am from the bank",
            "bank representative",
            "customer service",
            "fraud department",
            "government official",
            "police officer",
            "tax department",
            "technical support",
            "IT department",
            "security team",
            "official representative"
        ]
    },


    "emotional_manipulation": {

        "name": "Emotional Manipulation",

        "definition": (
            "Exploiting emotions such as guilt, sympathy, affection, "
            "shame, or fear to influence the target."
        ),

        "seed_terms": [
            "you should feel guilty",
            "after everything I have done for you",
            "you owe me",
            "don't disappoint me",
            "if you loved me",
            "you are hurting me",
            "I am disappointed in you",
            "feel sorry for me",
            "have some sympathy",
            "you should be ashamed",
            "I need you",
            "you are letting me down"
        ]
    },


    "financial_extraction": {

        "name": "Financial Extraction",

        "definition": (
            "Attempting to obtain money, payment credentials, banking "
            "information, OTPs, or other financially valuable information."
        ),

        "seed_terms": [
            "send money",
            "transfer money",
            "make a payment",
            "send the payment",
            "bank account",
            "credit card",
            "debit card",
            "card number",
            "banking information",
            "OTP",
            "verification code",
            "password",
            "PIN",
            "payment details"
        ]
    },


    "trust_engineering": {

        "name": "Trust Engineering",

        "definition": (
            "Gradually establishing credibility, familiarity, or trust "
            "in order to make later manipulation more effective."
        ),

        "seed_terms": [
            "I have been helping customers for years",
            "you can trust me",
            "I understand your situation",
            "I am here to help",
            "we have helped many people",
            "I have worked with you before",
            "as your trusted advisor",
            "I want to help you",
            "you are in safe hands",
            "we can take care of this for you"
        ]
    },


    "social_isolation": {

        "name": "Social Isolation",

        "definition": (
            "Discouraging the target from consulting or communicating "
            "with other people who could challenge the manipulation."
        ),

        "seed_terms": [
            "don't tell anyone",
            "keep this secret",
            "do not tell your family",
            "don't talk to anyone",
            "don't contact the bank",
            "keep this between us",
            "don't discuss this",
            "don't ask anyone",
            "you don't need anyone else",
            "handle this privately",
            "do not involve anyone"
        ]
    },


    "coercion": {

        "name": "Coercion",

        "definition": (
            "Using force, threats, pressure, or lack of meaningful "
            "choice to compel the target to perform an action."
        ),

        "seed_terms": [
            "you have no choice",
            "you must do this",
            "do it or else",
            "you cannot refuse",
            "you have to comply",
            "I will make you",
            "you must comply",
            "do exactly what I say",
            "there is no alternative",
            "you cannot say no",
            "you will do as I say"
        ]
    }
}


# ============================================================
# Display dictionary
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SAFEConv TACTIC DICTIONARY")
    print("=" * 70)

    print("\nNumber of tactics:", len(TACTICS))

    for tactic_id, tactic in TACTICS.items():

        print("\n" + "=" * 70)

        print("ID:", tactic_id)
        print("Name:", tactic["name"])

        print("\nDefinition:")
        print(tactic["definition"])

        print("\nSeed terms:")

        for term in tactic["seed_terms"]:
            print(" -", term)

        print("\nNumber of seed terms:",
              len(tactic["seed_terms"]))