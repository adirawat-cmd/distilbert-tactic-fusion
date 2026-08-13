CANDIDATES = {

    "urgency_pressure": [
        "don't delay",
        "without delay",
        "waste no time",
        "respond immediately",
        "respond promptly",
        "act without delay",
        "as soon as possible",
        "time is running out",
        "running out of time",
        "limited time",
        "take action now",
        "respond now",
        "do not hesitate",
        "quick response",
        "immediate action",
        "at your convenience",
        "take your time",
        "whenever you are ready"
    ],


    "fear_based_persuasion": [
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
        "everything could be lost",
        "nothing to worry about",
        "you are completely safe",
        "this is good news"
    ],


    "impersonation": [
        "I am a bank employee",
        "I am a banking representative",
        "I work for your bank",
        "I am from customer support",
        "I am a customer service agent",
        "I work for the government",
        "I am a police officer",
        "I am from the tax department",
        "I am from technical support",
        "I work in IT security",
        "I am an official representative",
        "I am just a friend",
        "I am your neighbor",
        "I am a stranger"
    ],


    "emotional_manipulation": [
        "you are making me feel guilty",
        "you should feel ashamed",
        "you are disappointing me",
        "you are hurting my feelings",
        "you don't care about me",
        "if you really loved me",
        "you owe me something",
        "I need your sympathy",
        "please feel sorry for me",
        "you are letting me down",
        "I appreciate your help",
        "I am happy for you",
        "you did a great job"
    ],


    "financial_extraction": [
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
        "tell me your account number",
        "have a nice day",
        "your account balance"
    ],


    "trust_engineering": [
        "you can rely on me",
        "you can trust me",
        "I have helped many customers",
        "I have years of experience",
        "I understand what you are going through",
        "I am here to support you",
        "we have helped people like you",
        "you are in good hands",
        "I will take care of everything",
        "we can handle this together",
        "I don't know you",
        "I cannot help you",
        "I am not familiar with this"
    ],


    "social_isolation": [
        "keep this private",
        "don't tell anyone",
        "don't tell your family",
        "don't contact anyone",
        "don't contact the bank",
        "don't discuss this with anyone",
        "keep this between us",
        "do not involve other people",
        "don't ask anyone for advice",
        "handle this yourself",
        "talk to your family",
        "ask your friend",
        "contact the bank",
        "tell someone you trust"
    ],


    "coercion": [
        "you must comply",
        "you have to do this",
        "you have no choice",
        "you cannot refuse",
        "you cannot say no",
        "do it or else",
        "I will force you",
        "you must follow my instructions",
        "do exactly what I tell you",
        "there is no alternative",
        "you are free to choose",
        "you can decide for yourself",
        "you don't have to do this"
    ]
}


if __name__ == "__main__":

    print("=" * 70)
    print("TACTIC CANDIDATE VOCABULARY")
    print("=" * 70)

    for tactic, candidates in CANDIDATES.items():

        print("\n" + "=" * 70)

        print("TACTIC:", tactic)

        print("Number of candidates:", len(candidates))

        for candidate in candidates:
            print(" -", candidate)