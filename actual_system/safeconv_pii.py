# import re
# from typing import Dict, List


# # ============================================================
# # SAFEConv PII MASKING
# # ============================================================
# #
# # Purpose:
# #   Detect common personally identifiable information (PII)
# #   in conversation text and replace it with neutral tokens.
# #
# # Example:
# #
# #   "Contact me at 9876543210"
# #
# # becomes:
# #
# #   "Contact me at <PHONE>"
# #
# # This module does NOT delete the surrounding message.
# # It only masks detected PII.
# #
# # IMPORTANT:
# # This is a practical runtime masking layer.
# # It is NOT a formal privacy/compliance guarantee.
# # ============================================================


# # ============================================================
# # PII PATTERNS
# # ============================================================

# PII_PATTERNS = {

#     "EMAIL": re.compile(
#         r"\b[a-zA-Z0-9._%+-]+"
#         r"@[a-zA-Z0-9.-]+\."
#         r"[a-zA-Z]{2,}\b"
#     ),

#     "URL": re.compile(
#         r"\b(?:https?://|www\.)"
#         r"[^\s<>]+"
#     ),

#     "IP_ADDRESS": re.compile(
#         r"\b(?:"
#         r"(?:25[0-5]|2[0-4]\d|"
#         r"1\d\d|[1-9]?\d)"
#         r"\.){3}"
#         r"(?:25[0-5]|2[0-4]\d|"
#         r"1\d\d|[1-9]?\d)"
#         r"\b"
#     ),

#     "PHONE": re.compile(
#         r"(?<!\d)"
#         r"(?:\+?\d{1,3}[\s.-]?)?"
#         r"(?:\(?\d{2,4}\)?[\s.-]?)?"
#         r"\d{3,4}[\s.-]?\d{3,4}"
#         r"(?!\d)"
#     ),

#     "CARD_NUMBER": re.compile(
#         r"(?<!\d)"
#         r"(?:\d[ -]?){13,19}"
#         r"(?!\d)"
#     )
# }


# # ============================================================
# # MASK ONE TEXT
# # ============================================================

# def mask_pii(
#     text: str
# ) -> Dict:

#     masked_text = text

#     detections: List[Dict] = []

#     # --------------------------------------------------------
#     # Process each PII category
#     # --------------------------------------------------------

#     for pii_type, pattern in PII_PATTERNS.items():

#         matches = list(
#             pattern.finditer(
#                 masked_text
#             )
#         )

#         for match in reversed(matches):

#             original_value = match.group()

#             start = match.start()
#             end = match.end()

#             replacement = (
#                 f"<{pii_type}>"
#             )

#             masked_text = (
#                 masked_text[:start]
#                 + replacement
#                 + masked_text[end:]
#             )

#             detections.append(
#                 {
#                     "type": pii_type,
#                     "value": original_value
#                 }
#             )

#     return {
#         "original_text": text,
#         "masked_text": masked_text,
#         "pii_detected": len(detections) > 0,
#         "detections": detections,
#         "detection_count": len(detections)
#     }


# # ============================================================
# # MASK MULTI-TURN CONVERSATION
# # ============================================================

# def mask_conversation(
#     conversation
# ):

#     # We import here to avoid circular imports.
#     from safeconv_conversation import Conversation

#     masked_conversation = Conversation()

#     all_detections = []

#     for turn in conversation.turns:

#         result = mask_pii(
#             turn.text
#         )

#         masked_conversation.add_turn(
#             speaker=turn.speaker,
#             text=result["masked_text"]
#         )

#         if result["pii_detected"]:

#             for detection in result[
#                 "detections"
#             ]:

#                 detection_with_turn = {
#                     "turn_id": turn.turn_id,
#                     "speaker": turn.speaker,
#                     "type": detection["type"],
#                     "value": detection["value"]
#                 }

#                 all_detections.append(
#                     detection_with_turn
#                 )

#     return {
#         "conversation":
#             masked_conversation,

#         "pii_detected":
#             len(all_detections) > 0,

#         "detections":
#             all_detections,

#         "detection_count":
#             len(all_detections)
#     }


# # ============================================================
# # TEST
# # ============================================================

# if __name__ == "__main__":

#     from safeconv_conversation import (
#         parse_conversation
#     )

#     sample_conversation = """
#     Person 1: Hello, my email is adi@example.com.
#     Person 2: You need to act immediately.
#     Person 1: My phone number is +91 9876543210.
#     Person 2: Send the information to https://example.com/login.
#     Person 1: The server IP is 192.168.1.10.
#     """

#     conversation = parse_conversation(
#         sample_conversation
#     )

#     result = mask_conversation(
#         conversation
#     )

#     print()
#     print("=" * 70)
#     print("SAFEConv PII MASKING TEST")
#     print("=" * 70)

#     print()

#     print("ORIGINAL CONVERSATION")
#     print("-" * 70)

#     for turn in conversation.turns:

#         print(
#             f"Turn {turn.turn_id} "
#             f"[{turn.speaker}]"
#         )

#         print(
#             f"  {turn.text}"
#         )

#     print()
#     print("MASKED CONVERSATION")
#     print("-" * 70)

#     masked_conversation = result[
#         "conversation"
#     ]

#     for turn in masked_conversation.turns:

#         print(
#             f"Turn {turn.turn_id} "
#             f"[{turn.speaker}]"
#         )

#         print(
#             f"  {turn.text}"
#         )

#     print()
#     print("PII DETECTIONS")
#     print("-" * 70)

#     for detection in result[
#         "detections"
#     ]:

#         print(
#             f"Turn {detection['turn_id']} "
#             f"[{detection['speaker']}]"
#         )

#         print(
#             f"  Type : "
#             f"{detection['type']}"
#         )

#         print(
#             f"  Value: "
#             f"{detection['value']}"
#         )

#     print()
#     print(
#         f"PII detected : "
#         f"{result['pii_detected']}"
#     )

#     print(
#         f"Detection count : "
#         f"{result['detection_count']}"
#     )

#     print()
#     print("=" * 70)
import re
from typing import Dict, List


# ============================================================
# SAFEConv PII MASKING
# ============================================================
#
# Detects common PII and replaces it with neutral placeholders.
#
# The runtime does NOT retain the original PII values.
#
# Example:
#
#   "Contact me at adi@example.com"
#
# becomes:
#
#   "Contact me at <EMAIL>"
#
# This is a practical prototype masking layer and is not a
# formal privacy/compliance guarantee.
# ============================================================


# ============================================================
# PII PATTERNS
# ============================================================

# PII_PATTERNS = {

#     "EMAIL": re.compile(
#         r"\b[a-zA-Z0-9._%+-]+"
#         r"@[a-zA-Z0-9.-]+\."
#         r"[a-zA-Z]{2,}\b"
#     ),

#     "URL": re.compile(
#         r"\b(?:https?://|www\.)"
#         r"[^\s<>]+"
#     ),

#     "IP_ADDRESS": re.compile(
#         r"\b(?:"
#         r"(?:25[0-5]|2[0-4]\d|"
#         r"1\d\d|[1-9]?\d)"
#         r"\.){3}"
#         r"(?:25[0-5]|2[0-4]\d|"
#         r"1\d\d|[1-9]?\d)"
#         r"\b"
#     ),

#     "CARD_NUMBER": re.compile(
#         r"(?<!\d)"
#         r"(?:\d[ -]?){13,19}"
#         r"(?!\d)"
#     ),

#     "PHONE": re.compile(
#         r"(?<!\d)"
#         r"(?:\+?\d{1,3}[\s.-]?)?"
#         r"(?:\(?\d{2,4}\)?[\s.-]?)?"
#         r"\d{3,4}[\s.-]?\d{3,4}"
#         r"(?!\d)"
#     )
# }

# ============================================================
# PII PATTERNS
# ============================================================

PII_PATTERNS = {

    "EMAIL": re.compile(
        r"\b[a-zA-Z0-9._%+-]+"
        r"@[a-zA-Z0-9.-]+\."
        r"[a-zA-Z]{2,}\b"
    ),

    "URL": re.compile(
        r"\b(?:https?://|www\.)"
        r"[^\s<>]+"
    ),

    "IP_ADDRESS": re.compile(
        r"\b(?:"
        r"(?:25[0-5]|2[0-4]\d|"
        r"1\d\d|[1-9]?\d)"
        r"\.){3}"
        r"(?:25[0-5]|2[0-4]\d|"
        r"1\d\d|[1-9]?\d)"
        r"\b"
    ),

    # --------------------------------------------------------
    # Account numbers
    # Examples:
    # 4587 2391 6642
    # 4587-2391-6642
    # --------------------------------------------------------
    "ACCOUNT_NUMBER": re.compile(
        r"(?<!\d)"
        r"\d{4}(?:[\s-]\d{4}){2,3}"
        r"(?!\d)"
    ),

    # --------------------------------------------------------
    # Card numbers
    # Examples:
    # 4111 1111 1111 1111
    # 4111-1111-1111-1111
    # --------------------------------------------------------
    "CARD_NUMBER": re.compile(
        r"(?<!\d)"
        r"(?:\d[ -]?){13,19}"
        r"(?!\d)"
    ),

    # --------------------------------------------------------
    # Indian phone numbers
    # Examples:
    # +91 9876543210
    # +91-9876543210
    # 9876543210
    # --------------------------------------------------------
    "PHONE": re.compile(
        r"(?<!\d)"
        r"(?:\+91[\s.-]?)?"
        r"[6-9]\d{9}"
        r"(?!\d)"
    )
}


# ============================================================
# CLEAN TRAILING URL PUNCTUATION
# ============================================================

def clean_url(value: str) -> str:

    return value.rstrip(
        ".,!?;:)]}>\"'"
    )


# ============================================================
# MASK ONE TEXT
# ============================================================

def mask_pii(
    text: str
) -> Dict:

    masked_text = text
    detections: List[Dict] = []

    # --------------------------------------------------------
    # Process PII categories
    # --------------------------------------------------------

    for pii_type, pattern in PII_PATTERNS.items():

        matches = list(
            pattern.finditer(
                masked_text
            )
        )

        for match in reversed(matches):

            original_value = match.group()

            # ------------------------------------------------
            # Clean punctuation from URLs
            # ------------------------------------------------

            if pii_type == "URL":

                cleaned_value = clean_url(
                    original_value
                )

                trailing_length = (
                    len(original_value)
                    - len(cleaned_value)
                )

                actual_end = (
                    match.end()
                    - trailing_length
                )

            else:

                actual_end = match.end()

            start = match.start()

            replacement = (
                f"<{pii_type}>"
            )

            masked_text = (
                masked_text[:start]
                + replacement
                + masked_text[actual_end:]
            )

            # ------------------------------------------------
            # IMPORTANT:
            #
            # Do NOT store original_value.
            #
            # Only metadata is retained.
            # ------------------------------------------------

            detections.append(
                {
                    "type": pii_type,
                    "placeholder": replacement
                }
            )

    return {

        "masked_text":
            masked_text,

        "pii_detected":
            len(detections) > 0,

        "detections":
            detections,

        "detection_count":
            len(detections)
    }


# ============================================================
# MASK MULTI-TURN CONVERSATION
# ============================================================

def mask_conversation(
    conversation
):

    from safeconv_conversation import Conversation

    masked_conversation = Conversation()

    all_detections = []

    for turn in conversation.turns:

        result = mask_pii(
            turn.text
        )

        masked_conversation.add_turn(
            speaker=turn.speaker,
            text=result["masked_text"]
        )

        for detection in result[
            "detections"
        ]:

            all_detections.append(
                {
                    "turn_id":
                        turn.turn_id,

                    "speaker":
                        turn.speaker,

                    "type":
                        detection["type"],

                    "placeholder":
                        detection["placeholder"]
                }
            )

    return {

        "conversation":
            masked_conversation,

        "pii_detected":
            len(all_detections) > 0,

        "detections":
            all_detections,

        "detection_count":
            len(all_detections)
    }




if __name__ == "__main__":

    from safeconv_conversation import (
        parse_conversation
    )

    sample_conversation = """
    Person 1: Hello, my email is adi@example.com.
    Person 2: You need to act immediately.
    Person 1: My phone number is +91 9876543210.
    Person 2: Send the information to https://example.com/login.
    Person 1: The server IP is 192.168.1.10.
    """

    conversation = parse_conversation(
        sample_conversation
    )

    result = mask_conversation(
        conversation
    )

    print()
    print("=" * 70)
    print("SAFEConv PII MASKING TEST")
    print("=" * 70)

    print()
    print("MASKED CONVERSATION")
    print("-" * 70)

    for turn in result[
        "conversation"
    ].turns:

        print(
            f"Turn {turn.turn_id} "
            f"[{turn.speaker}]"
        )

        print(
            f"  {turn.text}"
        )

    print()
    print("PII METADATA")
    print("-" * 70)

    for detection in result[
        "detections"
    ]:

        print(
            f"Turn {detection['turn_id']} "
            f"[{detection['speaker']}] "
            f"{detection['type']} "
            f"-> "
            f"{detection['placeholder']}"
        )

    print()
    print(
        f"PII detected : "
        f"{result['pii_detected']}"
    )

    print(
        f"Detection count : "
        f"{result['detection_count']}"
    )

    print()
    print("=" * 70)