
from safeconv_runtime import SAFEConvRuntime

runtime = SAFEConvRuntime()

cases = {
    "A - Ordinary conversation": """
Person 1: I want to open a savings account.
Person 2: You can review the requirements on our official website.
Person 1: What documents do I need?
Person 2: Please review the checklist and contact the branch if you need help.
""",
    "B - Ambiguous urgency": """
Person 1: Can you review this work request?
Person 2: Please respond as soon as possible because the deadline is today.
Person 1: I will review it and get back to you.
Person 2: Thank you. Let me know if you need more information.
""",
    "C - Social engineering": """
Person 1: Why are you calling?
Person 2: I am from your bank security department.
Person 2: Your account will be frozen unless you send me your OTP immediately.
Person 1: Can I contact the bank directly?
Person 2: No. Do not contact anyone else. Send me the code now.
"""
}

for name, conversation in cases.items():
    result = runtime.analyze(conversation)

    print(f"\n{'=' * 60}")
    print(name)
    print("=" * 60)

    print("Temporal risk:", result["model"]["risk_probability"])
    print("Behavioral tactics:", result["behavior"]["active_tactics"])
    print("Behavioral score:", result["risk_assessment"]["behavioral_score"])
    print("Final risk:", result["risk_assessment"]["risk_score"])
    print("Risk level:", result["risk_assessment"]["risk_level"])

    print("Semantic features:")
    for tactic, score in zip(
        result["semantic_tactics"]["tactic_order"],
        result["semantic_tactics"]["features"]
    ):
        print(f"  {tactic}: {score:.4f}")
