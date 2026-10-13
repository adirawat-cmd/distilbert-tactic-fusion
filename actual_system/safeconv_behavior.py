import re
from typing import Dict, List

from safeconv_conversation import Conversation


# ============================================================
# SAFEConv BEHAVIORAL TACTICS
# ============================================================

TACTICS = [
    "urgency_pressure",
    "fear_based_persuasion",
    "impersonation",
    "emotional_manipulation",
    "financial_extraction",
    "trust_engineering",
    "social_isolation",
    "coercion"
]


# ============================================================
# BEHAVIORAL INDICATORS
# ============================================================
#
# These are runtime indicators, NOT proof that a tactic
# definitely exists.
#
# We deliberately keep the detector conservative because
# the dataset audit showed that some individual terms can
# produce false positives when used without context.
#
# Phrase matching is therefore used where possible.
# ============================================================

BEHAVIORAL_PATTERNS = {

    "urgency_pressure": [

        r"\bact now\b",
        r"\bdo it now\b",
        r"\bright now\b",
        r"\bimmediately\b",
        r"\burgent(?:ly)?\b",
        r"\bquickly\b",
        r"\bdon't wait\b",
        r"\bdo not wait\b",
        r"\btime is running out\b",
        r"\blast chance\b",
        r"\bbefore it's too late\b",
        r"\byou need to act\b",
        r"\byou need to do this now\b",
        r"\bwithin \d+ (?:minutes?|hours?)\b",
        r"\bdeadline\b"
    ],

    "fear_based_persuasion": [

        r"\byour account has been compromised\b",
        r"\byour account has been hacked\b",
        r"\byour account is hacked\b",
        r"\byour account will be\b",
        r"\byou will lose\b",
        r"\byou could lose\b",
        r"\byou are in danger\b",
        r"\byou're in danger\b",
        r"\bsecurity (?:alert|threat|breach)\b",
        r"\byour information is at risk\b",
        r"\byour data is at risk\b",
        r"\bpolice will\b",
        r"\byou will be arrested\b",
        r"\byou could be arrested\b",
        r"\byou'll be arrested\b",
        r"\blegal action\b",
        r"\baccount will be closed\b",
        r"\baccount may be closed\b"
    ],

    "impersonation": [

        r"\bi am from (?:the )?(?:bank|police|government|support|security)\b",
        r"\bi'm from (?:the )?(?:bank|police|government|support|security)\b",
        r"\bthis is (?:the )?(?:bank|police|government|support|security)\b",
        r"\bcalling from (?:the )?(?:bank|police|government|support|security)\b",
        r"\bi work for (?:the )?(?:bank|police|government|company)\b",
        r"\bi am your (?:bank|account|security) representative\b",
        r"\bi'm your (?:bank|account|security) representative\b",
        r"\bofficial (?:support|security) team\b",
        r"\bcustomer support\b",
        r"\bsecurity team\b"
    ],

    "emotional_manipulation": [

        r"\bif you love me\b",
        r"\bif you really love me\b",
        r"\bprove you love me\b",
        r"\bdo this for me\b",
        r"\bplease don't leave me\b",
        r"\byou don't care about me\b",
        r"\byou don't trust me\b",
        r"\bafter everything i've done\b",
        r"\bafter everything i have done\b",
        r"\bi thought you loved me\b",
        r"\bi thought you cared\b",
        r"\byou're hurting me\b",
        r"\byou are hurting me\b"
    ],

    "financial_extraction": [

        r"\bsend me (?:the )?(?:money|cash)\b",
        r"\btransfer (?:the )?(?:money|funds)\b",
        r"\bsend (?:the )?(?:money|funds)\b",
        r"\bpay me\b",
        r"\bmake a payment\b",
        r"\bwire (?:the )?money\b",
        r"\bdeposit (?:the )?(?:money|funds)\b",
        r"\bgift card\b",
        r"\bbitcoin\b",
        r"\bcrypto(?:currency)?\b",
        r"\bbank transfer\b",
        r"\baccount number\b",
        r"\bbank details\b",
        r"\bcard number\b",
        r"\bcredit card\b",
        r"\bdebit card\b"
    ],

    "trust_engineering": [

        r"\byou can trust me\b",
        r"\btrust me\b",
        r"\byou can rely on me\b",
        r"\bi promise\b",
        r"\bi swear\b",
        r"\bbetween you and me\b",
        r"\bkeep this between us\b",
        r"\bthis is confidential\b",
        r"\bno one else needs to know\b",
        r"\byou can tell me anything\b",
        r"\bi'm here to help\b",
        r"\bi am here to help\b"
    ],

    "social_isolation": [

        r"\bdon't tell anyone\b",
        r"\bdo not tell anyone\b",
        r"\bdon't tell your family\b",
        r"\bdo not tell your family\b",
        r"\bdon't tell your friends\b",
        r"\bdo not tell your friends\b",
        r"\bkeep this secret\b",
        r"\bkeep it secret\b",
        r"\bkeep this between us\b",
        r"\btell nobody\b",
        r"\btell no one\b",
        r"\bno one else\b",
        r"\bjust between us\b"
    ],

    "coercion": [

        r"\byou must\b",
        r"\byou have to\b",
        r"\byou need to\b",
        r"\bdo it or\b",
        r"\bif you don't\b",
        r"\bif you do not\b",
        r"\bi will report you\b",
        r"\bi'll report you\b",
        r"\bi will expose you\b",
        r"\bi'll expose you\b",
        r"\bi will tell everyone\b",
        r"\bi'll tell everyone\b",
        r"\byou have no choice\b",
        r"\bno choice\b",
        r"\bdo as i say\b",
        r"\bdo what i say\b"
    ]
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text: str) -> str:

    text = text.lower()

    # Normalize repeated whitespace.
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# MATCH INDICATORS
# ============================================================

def find_matches(
    text: str,
    patterns: List[str]
) -> List[str]:

    normalized = normalize_text(text)

    matches = []

    for pattern in patterns:

        if re.search(
            pattern,
            normalized
        ):

            matches.append(pattern)

    return matches


# ============================================================
# ANALYZE ONE TURN
# ============================================================

def analyze_turn(
    text: str,
    turn_id: int,
    speaker: str
) -> Dict:

    evidence = []

    tactic_matches = {}

    for tactic in TACTICS:

        patterns = BEHAVIORAL_PATTERNS[
            tactic
        ]

        matches = find_matches(
            text,
            patterns
        )

        if matches:

            tactic_matches[tactic] = len(
                matches
            )

            evidence.append(
                {
                    "turn_id": turn_id,
                    "speaker": speaker,
                    "tactic": tactic,
                    "text": text,
                    "match_count": len(matches)
                }
            )

    return {
        "turn_id": turn_id,
        "speaker": speaker,
        "tactic_matches": tactic_matches,
        "evidence": evidence
    }


# ============================================================
# ANALYZE ENTIRE CONVERSATION
# ============================================================

def analyze_behavior(
    conversation: Conversation
) -> Dict:

    tactic_counts = {
        tactic: 0
        for tactic in TACTICS
    }

    tactic_turns = {
        tactic: []
        for tactic in TACTICS
    }

    evidence = []

    # --------------------------------------------------------
    # Analyze every turn
    # --------------------------------------------------------

    turn_results = []

    for turn in conversation.turns:

        result = analyze_turn(
            text=turn.text,
            turn_id=turn.turn_id,
            speaker=turn.speaker
        )

        turn_results.append(
            result
        )

        for tactic, count in result[
            "tactic_matches"
        ].items():

            tactic_counts[tactic] += count

            tactic_turns[tactic].append(
                turn.turn_id
            )

        evidence.extend(
            result["evidence"]
        )

    # --------------------------------------------------------
    # Convert counts into bounded tactic scores
    # --------------------------------------------------------
    #
    # The score is an evidence score, NOT a probability.
    #
    # 0.0 = no indicator detected
    # 1.0 = strong amount of indicator evidence
    #
    # We cap the score at 1.0.
    # --------------------------------------------------------

    tactic_scores = {}

    for tactic in TACTICS:

        count = tactic_counts[tactic]

        tactic_scores[tactic] = min(
            count / 2.0,
            1.0
        )

    # --------------------------------------------------------
    # Active tactics
    # --------------------------------------------------------

    active_tactics = [
        tactic
        for tactic in TACTICS
        if tactic_counts[tactic] > 0
    ]

    # --------------------------------------------------------
    # Total behavioral activity
    # --------------------------------------------------------

    total_matches = sum(
        tactic_counts.values()
    )

    active_tactic_ratio = (
        len(active_tactics) / len(TACTICS)
    )

    return {

        "tactic_scores": tactic_scores,

        "tactic_counts": tactic_counts,

        "active_tactics": active_tactics,

        "active_tactic_count": len(
            active_tactics
        ),

        "active_tactic_ratio":
            active_tactic_ratio,

        "total_matches":
            total_matches,

        "evidence":
            evidence,

        "turn_results":
            turn_results
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    from safeconv_conversation import (
        parse_conversation
    )

    sample_conversation = """
    Person 1: Hello, I received your message.
    Person 2: Yes, I need your help immediately.
    Person 1: What happened?
    Person 2: Your account has been compromised.
    Person 1: What should I do?
    Person 2: Send me the verification code now.
    """

    conversation = parse_conversation(
        sample_conversation
    )

    result = analyze_behavior(
        conversation
    )

    print()
    print("=" * 70)
    print("SAFEConv BEHAVIORAL ANALYSIS TEST")
    print("=" * 70)

    print()
    print("TACTIC SCORES")
    print("-" * 70)

    for tactic, score in result[
        "tactic_scores"
    ].items():

        print(
            f"{tactic:<28} "
            f"{score:.2f}"
        )

    print()
    print("ACTIVE TACTICS")
    print("-" * 70)

    if result["active_tactics"]:

        for tactic in result[
            "active_tactics"
        ]:

            print(
                f"- {tactic}"
            )

    else:

        print("None")

    print()
    print("EVIDENCE")
    print("-" * 70)

    if result["evidence"]:

        for item in result["evidence"]:

            print(
                f"Turn {item['turn_id']} "
                f"[{item['speaker']}]"
            )

            print(
                f"  Tactic: "
                f"{item['tactic']}"
            )

            print(
                f"  Text: "
                f"{item['text']}"
            )

            print(
                f"  Matches: "
                f"{item['match_count']}"
            )

            print()

    else:

        print("No behavioral indicators detected.")

    print()
    print(
        f"Total matches: "
        f"{result['total_matches']}"
    )

    print(
        f"Active tactic count: "
        f"{result['active_tactic_count']}"
    )

    print(
        f"Active tactic ratio: "
        f"{result['active_tactic_ratio']:.2f}"
    )

    print()
    print("=" * 70)