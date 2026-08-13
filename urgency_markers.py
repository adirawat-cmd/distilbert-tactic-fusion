URGENCY_MARKERS = {
    "immediacy": [
        "immediately",
        "right now",
        "right away",
        "at once",
        "now"
    ],

    "speed_pressure": [
        "hurry",
        "hurry up",
        "act fast",
        "act quickly",
        "don't wait",
        "do it quickly"
    ],

    "deadline": [
        "deadline",
        "within",
        "before",
        "expires",
        "expires today",
        "last chance",
        "final warning"
    ],

    "time_constraint": [
        "within 5 minutes",
        "within 10 minutes",
        "within an hour",
        "today only",
        "before midnight",
        "before it's too late"
    ],

    "urgency_adjectives": [
        "urgent",
        "critical",
        "immediate",
        "pressing",
        "time-sensitive"
    ]
}


if __name__ == "__main__":

    print("Urgency marker categories:",
          len(URGENCY_MARKERS))

    total_markers = sum(
        len(markers)
        for markers in URGENCY_MARKERS.values()
    )

    print("Total initial markers:", total_markers)

    for category, markers in URGENCY_MARKERS.items():

        print("\n" + "=" * 60)

        print("Category:", category)

        print("Markers:")

        for marker in markers:
            print(" -", marker)