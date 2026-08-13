import re


URGENCY_MARKERS = [
    "immediately",
    "right now",
    "right away",
    "at once",
    "now",

    "hurry",
    "hurry up",
    "act fast",
    "act quickly",
    "don't wait",
    "do it quickly",

    "deadline",
    "within",
    "before",
    "expires",
    "expires today",
    "last chance",
    "final warning",

    "within 5 minutes",
    "within 10 minutes",
    "within an hour",
    "today only",
    "before midnight",
    "before it's too late",

    "urgent",
    "critical",
    "immediate",
    "pressing",
    "time-sensitive",

    # Newly validated semantic candidates
    "promptly",
    "act without delay",
    "quickly",
    "respond immediately",
    "soon",
    "rapidly",
    "as soon as possible",
    "respond promptly",
    "immediate action",
    "without delay"
]


# def detect_urgency_markers(text):

#     text_lower = text.lower()

#     detected = []

#     for marker in URGENCY_MARKERS:

#         if marker in text_lower:

#             detected.append(marker)

#     return detected


def detect_urgency_markers(text):

    text_lower = text.lower()

    detected = []

    # Sort longer phrases first
    # so "respond promptly" is checked before "promptly"
    sorted_markers = sorted(
        URGENCY_MARKERS,
        key=len,
        reverse=True
    )

    for marker in sorted_markers:

        # Escape special regex characters
        pattern = r"\b" + re.escape(marker.lower()) + r"\b"

        if re.search(pattern, text_lower):

            detected.append(marker)

    # Remove overlapping markers
    final_detected = []

    for marker in detected:

        marker_is_part_of_existing = False

        for existing in final_detected:

            if marker in existing:
                marker_is_part_of_existing = True
                break

        if not marker_is_part_of_existing:
            final_detected.append(marker)

    return final_detected


# --------------------------------------------------
# Test conversations
# --------------------------------------------------

test_conversations = [

    "Your account will be closed unless you act immediately.",

    "You have only 10 minutes to complete the payment.",

    "Please respond promptly so that we can process your request.",

    "I hope you have a good day. Please contact me whenever convenient.",

    "This is your final warning. Your account expires today."
]


for i, conversation in enumerate(test_conversations, 1):

    detected = detect_urgency_markers(conversation)

    print("\n" + "=" * 70)

    print("Conversation:")
    print(conversation)

    print("\nDetected markers:")

    if detected:
        for marker in detected:
            print(" -", marker)
    else:
        print(" None")