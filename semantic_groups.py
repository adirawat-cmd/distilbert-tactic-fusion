SEMANTIC_GROUPS = {

    "urgency_pressure": {

        "immediacy": [
            "urgent",
            "immediately",
            "right now",
            "right away",
            "act now",
            "immediate action",
            "respond immediately"
        ],

        "speed_pressure": [
            "act fast",
            "hurry",
            "don't delay",
            "without delay",
            "waste no time",
            "respond promptly",
            "act without delay",
            "as soon as possible",
            "respond now"
        ],

        "deadline": [
            "deadline",
            "last chance",
            "final warning",
            "expires today"
        ],

        "time_constraint": [
            "limited time",
            "within minutes",
            "time-sensitive",
            "time is running out",
            "running out of time"
        ]
    },


    "fear_based_persuasion": {

        "threat": [
            "threat",
            "security threat",
            "danger",
            "warning",
            "you are at risk",
            "your account is at risk"
        ],

        "negative_consequence": [
            "you will be blocked",
            "your account will be suspended",
            "your account may be locked",
            "you may lose access",
            "you will lose your money",
            "you could lose everything",
            "everything could be lost",
            "you could face consequences",
            "negative consequences",
            "you could be punished"
        ],

        "legal_or_authority_threat": [
            "legal action",
            "you will face legal action",
            "you will be arrested",
            "you could be in trouble"
        ]
    },


    "impersonation": {

        "banking": [
            "I am calling from your bank",
            "I am from the bank",
            "bank representative",
            "I am a bank employee",
            "I am a banking representative",
            "I work for your bank",
            "fraud department"
        ],

        "government_authority": [
            "government official",
            "official representative",
            "I work for the government",
            "police officer",
            "tax department",
            "I am from the tax department",
            "I am an official representative"
        ],

        "technical_support": [
            "technical support",
            "IT department",
            "security team",
            "I am from technical support",
            "I work in IT security"
        ],

        "customer_service": [
            "customer service",
            "I am from customer support",
            "I am a customer service agent"
        ]
    },


    "emotional_manipulation": {

        "guilt": [
            "you should feel guilty",
            "you are making me feel guilty",
            "you owe me",
            "you owe me something",
            "after everything I have done for you"
        ],

        "shame": [
            "you should be ashamed",
            "you should feel ashamed",
            "don't disappoint me",
            "you are disappointing me"
        ],

        "sympathy": [
            "feel sorry for me",
            "please feel sorry for me",
            "have some sympathy",
            "I need your sympathy"
        ],

        "emotional_blame": [
            "you are hurting me",
            "you are hurting my feelings",
            "you are letting me down",
            "I am disappointed in you"
        ],

        "affection_pressure": [
            "if you loved me",
            "if you really loved me",
            "I need you"
        ]
    },


    "financial_extraction": {

        "payment": [
            "send money",
            "transfer money",
            "make a payment",
            "send the payment",
            "transfer the funds",
            "send the funds",
            "wire the money",
            "make the transfer"
        ],

        "banking_information": [
            "bank account",
            "banking information",
            "provide your bank details",
            "send your banking information",
            "tell me your account number",
            "card number",
            "give me your card number"
        ],

        "payment_cards": [
            "credit card",
            "debit card",
            "provide your credit card information"
        ],

        "authentication_credentials": [
            "OTP",
            "verification code",
            "give me the verification code",
            "send me the OTP",
            "PIN",
            "provide your PIN",
            "password",
            "share your password"
        ],

        "payment_details": [
            "payment details"
        ]
    },


    "trust_engineering": {

        "credibility": [
            "I have been helping customers for years",
            "I have helped many customers",
            "I have years of experience",
            "we have helped many people",
            "we have helped people like you"
        ],

        "trust_building": [
            "you can trust me",
            "you can rely on me",
            "you are in safe hands",
            "you are in good hands",
            "as your trusted advisor"
        ],

        "support": [
            "I am here to help",
            "I want to help you",
            "I am here to support you",
            "I understand your situation",
            "I understand what you are going through"
        ],

        "assurance": [
            "we can take care of this for you",
            "I will take care of everything",
            "we can handle this together",
            "I have worked with you before"
        ]
    },


    "social_isolation": {

        "secrecy": [
            "don't tell anyone",
            "keep this secret",
            "keep this between us",
            "keep this private",
            "don't discuss this",
            "don't discuss this with anyone"
        ],

        "preventing_consultation": [
            "don't ask anyone",
            "don't ask anyone for advice",
            "don't talk to anyone",
            "don't contact anyone",
            "do not involve anyone",
            "do not involve other people"
        ],

        "preventing_external_verification": [
            "don't contact the bank",
            "do not tell your family",
            "you don't need anyone else"
        ],

        "self_containment": [
            "handle this privately",
            "handle this yourself"
        ]
    },


    "coercion": {

        "lack_of_choice": [
            "you have no choice",
            "there is no alternative",
            "you cannot refuse",
            "you cannot say no"
        ],

        "forced_compliance": [
            "you must do this",
            "you must comply",
            "you have to comply",
            "you have to do this",
            "you must follow my instructions"
        ],

        "direct_command": [
            "do exactly what I say",
            "do exactly what I tell you",
            "you will do as I say"
        ],

        "threat_of_force": [
            "do it or else",
            "I will make you",
            "I will force you"
        ]
    }
}


if __name__ == "__main__":

    print("=" * 70)
    print("SEMANTIC TACTIC GROUPS")
    print("=" * 70)

    total_groups = 0
    total_terms = 0

    for tactic, groups in SEMANTIC_GROUPS.items():

        print("\n" + "=" * 70)
        print(tactic)

        for group_name, terms in groups.items():

            print("\n[" + group_name + "]")

            for term in terms:
                print(" -", term)

            total_groups += 1
            total_terms += len(terms)

    print("\n" + "=" * 70)
    print("TOTAL SEMANTIC GROUPS:", total_groups)
    print("TOTAL GROUPED TERMS:", total_terms)