VALIDATED_TACTICS = {

    "urgency_pressure": [
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
        "within minutes",
        "don't delay",
        "without delay",
        "waste no time",
        "respond immediately",
        "respond promptly",
        "act without delay",
        "as soon as possible",
        "time is running out",
        "running out of time",
        "take action now",
        "respond now",
        "immediate action"
    ],


    "fear_based_persuasion": [
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
        "you could lose everything",
        "you could be in trouble",
        "your account is in danger",
        "you could face consequences",
        "you will face legal action",
        "your account may be locked",
        "you may lose access",
        "this could cause serious problems",
        "you could be punished",
        "you are at risk",
        "there is a security threat",
        "everything could be lost"
    ],


    "impersonation": [
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
        "official representative",
        "I am a bank employee",
        "I am a banking representative",
        "I work for your bank",
        "I am from customer support",
        "I am a customer service agent",
        "I work for the government",
        "I am from the tax department",
        "I am from technical support",
        "I work in IT security",
        "I am an official representative"
    ],


    "emotional_manipulation": [
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
        "you are letting me down",
        "you are making me feel guilty",
        "if you really loved me",
        "you should feel ashamed",
        "you owe me something",
        "please feel sorry for me",
        "I need your sympathy",
        "you are hurting my feelings",
        "you are disappointing me"
    ],


    "financial_extraction": [
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
        "payment details",
        "transfer the funds",
        "send the funds",
        "wire the money",
        "make the transfer",
        "provide your bank details",
        "give me your card number",
        "provide your credit card information",
        "send your banking information",
        "give me the verification code",
        "send me the OTP",
        "provide your PIN",
        "share your password",
        "tell me your account number"
    ],


    "trust_engineering": [
        "I have been helping customers for years",
        "you can trust me",
        "I understand your situation",
        "I am here to help",
        "we have helped many people",
        "I have worked with you before",
        "as your trusted advisor",
        "I want to help you",
        "you are in safe hands",
        "we can take care of this for you",
        "you can rely on me",
        "I have helped many customers",
        "we have helped people like you",
        "you are in good hands",
        "I understand what you are going through",
        "I will take care of everything",
        "I am here to support you",
        "we can handle this together"
    ],


    "social_isolation": [
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
        "do not involve anyone",
        "keep this private",
        "don't contact anyone",
        "don't discuss this with anyone",
        "keep this between us",
        "do not involve other people",
        "don't ask anyone for advice",
        "handle this yourself"
    ],


    "coercion": [
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
        "you will do as I say",
        "you have to do this",
        "I will force you",
        "you must follow my instructions",
        "do exactly what I tell you"
    ]
}


if __name__ == "__main__":

    print("=" * 70)
    print("VALIDATED TACTIC DICTIONARY")
    print("=" * 70)

    total = 0

    for tactic, terms in VALIDATED_TACTICS.items():

        print("\n" + "=" * 70)
        print(tactic)
        print("Number of terms:", len(terms))

        for term in terms:
            print(" -", term)

        total += len(terms)

    print("\n" + "=" * 70)
    print("TOTAL TERMS:", total)