TACTICS = {
    "urgency_pressure": {
        "name": "Urgency Pressure",
        "definition": (
            "Creating time pressure or a sense of immediate action "
            "to discourage the target from thinking or verifying information."
        ),
        "examples": [
            "Act immediately or your account will be blocked.",
            "You only have five minutes to complete the payment.",
            "You need to do this right now."
        ]
    },

    "fear_based_persuasion": {
        "name": "Fear-Based Persuasion",
        "definition": (
            "Using threats, danger, negative consequences, or fear "
            "to influence the target's behavior."
        ),
        "examples": [
            "Your account will be suspended if you do not comply.",
            "You could face legal action if you don't respond.",
            "Something bad will happen if you ignore this."
        ]
    },

    "impersonation": {
        "name": "Impersonation",
        "definition": (
            "Pretending to be a trusted person, organization, authority, "
            "or service in order to gain credibility."
        ),
        "examples": [
            "I am calling from your bank's fraud department.",
            "This is the police cybercrime division.",
            "I am from the company's HR department."
        ]
    },

    "emotional_manipulation": {
        "name": "Emotional Manipulation",
        "definition": (
            "Exploiting emotions such as guilt, sympathy, affection, "
            "shame, or fear to influence the target."
        ),
        "examples": [
            "After everything I have done for you, you owe me this.",
            "If you really cared about me, you would help.",
            "Please don't abandon me when I need you."
        ]
    },

    "financial_extraction": {
        "name": "Financial Extraction",
        "definition": (
            "Attempting to obtain money, payment credentials, banking "
            "information, OTPs, or other financially valuable information."
        ),
        "examples": [
            "Send the payment to this account.",
            "Tell me the OTP to verify your transaction.",
            "Transfer the money before the deadline."
        ]
    },

    "trust_engineering": {
        "name": "Trust Engineering",
        "definition": (
            "Gradually establishing credibility, familiarity, or trust "
            "in order to make later manipulation more effective."
        ),
        "examples": [
            "I have been helping customers like you for years.",
            "You can trust me; I am here to protect your account.",
            "We have been working together for a long time."
        ]
    },

    "social_isolation": {
        "name": "Social Isolation",
        "definition": (
            "Discouraging the target from consulting or communicating "
            "with other people who could challenge the manipulation."
        ),
        "examples": [
            "Don't tell anyone about this.",
            "You should handle this yourself.",
            "Do not contact the bank directly."
        ]
    },

    "coercion": {
        "name": "Coercion",
        "definition": (
            "Using force, threats, pressure, or lack of meaningful choice "
            "to compel the target to perform an action."
        ),
        "examples": [
            "You have no choice but to do this.",
            "Do exactly what I tell you.",
            "If you refuse, there will be consequences."
        ]
    }
}


if __name__ == "__main__":
    print("Number of tactics:", len(TACTICS))

    for key, tactic in TACTICS.items():
        print("\n" + "=" * 60)
        print("ID:", key)
        print("Name:", tactic["name"])
        print("Definition:", tactic["definition"])
        print("Example:", tactic["examples"][0])