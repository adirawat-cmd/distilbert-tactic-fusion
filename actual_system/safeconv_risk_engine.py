# from typing import Dict, List

# from safeconv_state import ConversationState


# # ============================================================
# # SAFEConv RISK ENGINE
# # ============================================================
# #
# # This is a transparent decision layer.
# #
# # It does NOT replace the trained DistilBERT + BiLSTM model.
# #
# # It combines:
# #
# #   1. Temporal model risk
# #   2. Behavioral evidence
# #
# # and converts them into a human-readable risk assessment.
# #
# # The weights and risk bands below are INITIAL ENGINEERING
# # PARAMETERS. They are not claimed to be statistically
# # calibrated.
# # ============================================================


# TEMPORAL_WEIGHT = 0.70
# BEHAVIORAL_WEIGHT = 0.30

# TOTAL_TACTICS = 8


# # ============================================================
# # RISK LEVELS
# # ============================================================

# def get_risk_level(
#     risk_score: float
# ) -> str:

#     if risk_score >= 0.80:

#         return "CRITICAL"

#     elif risk_score >= 0.60:

#         return "HIGH"

#     elif risk_score >= 0.30:

#         return "MEDIUM"

#     else:

#         return "LOW"


# # ============================================================
# # BEHAVIORAL SCORE
# # ============================================================

# def calculate_behavioral_score(
#     state: ConversationState
# ) -> float:

#     if TOTAL_TACTICS == 0:

#         return 0.0

#     active_tactic_count = len(
#         state.active_tactics
#     )

#     score = (
#         active_tactic_count
#         / TOTAL_TACTICS
#     )

#     return min(
#         max(score, 0.0),
#         1.0
#     )


# # ============================================================
# # EVIDENCE SUMMARY
# # ============================================================

# def build_evidence_summary(
#     state: ConversationState
# ) -> List[Dict]:

#     evidence_summary = []

#     for evidence in (
#         state.behavioral_evidence
#     ):

#         evidence_summary.append(
#             {
#                 "turn_id":
#                     evidence.get(
#                         "turn_id"
#                     ),

#                 "speaker":
#                     evidence.get(
#                         "speaker"
#                     ),

#                 "tactic":
#                     evidence.get(
#                         "tactic"
#                     ),

#                 "text":
#                     evidence.get(
#                         "text"
#                     )
#             }
#         )

#     return evidence_summary


# # ============================================================
# # RISK ENGINE
# # ============================================================

# class BehavioralRiskEngine:

#     def __init__(
#         self,
#         temporal_weight=TEMPORAL_WEIGHT,
#         behavioral_weight=BEHAVIORAL_WEIGHT
#     ):

#         self.temporal_weight = (
#             temporal_weight
#         )

#         self.behavioral_weight = (
#             behavioral_weight
#         )

#         total_weight = (
#             self.temporal_weight
#             + self.behavioral_weight
#         )

#         if abs(total_weight - 1.0) > 1e-6:

#             raise ValueError(
#                 "Risk engine weights must "
#                 "sum to 1.0."
#             )

#     # ========================================================
#     # ANALYZE
#     # ========================================================

#     def analyze(
#         self,
#         state: ConversationState
#     ) -> Dict:

#         # ----------------------------------------------------
#         # Temporal signal
#         # ----------------------------------------------------

#         temporal_score = min(
#             max(
#                 float(
#                     state.temporal_risk
#                 ),
#                 0.0
#             ),
#             1.0
#         )

#         # ----------------------------------------------------
#         # Behavioral signal
#         # ----------------------------------------------------

#         behavioral_score = (
#             calculate_behavioral_score(
#                 state
#             )
#         )

#         # ----------------------------------------------------
#         # Combined risk score
#         # ----------------------------------------------------

#         final_score = (
#             self.temporal_weight
#             * temporal_score
#             +
#             self.behavioral_weight
#             * behavioral_score
#         )

#         final_score = min(
#             max(final_score, 0.0),
#             1.0
#         )

#         # ----------------------------------------------------
#         # Risk level
#         # ----------------------------------------------------

#         risk_level = get_risk_level(
#             final_score
#         )

#         # ----------------------------------------------------
#         # Evidence
#         # ----------------------------------------------------

#         evidence = build_evidence_summary(
#             state
#         )

#         # ----------------------------------------------------
#         # Return assessment
#         # ----------------------------------------------------

#         return {

#             "risk_score":
#                 final_score,

#             "risk_level":
#                 risk_level,

#             "temporal_score":
#                 temporal_score,

#             "behavioral_score":
#                 behavioral_score,

#             "temporal_weight":
#                 self.temporal_weight,

#             "behavioral_weight":
#                 self.behavioral_weight,

#             "active_tactics":
#                 list(
#                     state.active_tactics
#                 ),

#             "active_tactic_count":
#                 len(
#                     state.active_tactics
#                 ),

#             "evidence":
#                 evidence,

#             "escalation_detected":
#                 state.escalation_detected,

#             "escalation_score":
#                 state.escalation_score
#         }


# # ============================================================
# # TEST
# # ============================================================

# if __name__ == "__main__":

#     state = ConversationState()

#     # Real temporal-model result obtained from the
#     # current SAFEConv runtime test.
#     state.update_temporal(
#         risk_probability=0.8968,
#         turn_count=6,
#         analyzed_turns=6,
#         truncated=False
#     )

#     # Real behavioral evidence obtained from the
#     # current SAFEConv behavioral test.
#     state.update_behavioral(

#         tactic_scores={
#             "urgency_pressure": 0.50,
#             "fear_based_persuasion": 0.50,
#             "impersonation": 0.00,
#             "emotional_manipulation": 0.00,
#             "financial_extraction": 0.00,
#             "trust_engineering": 0.00,
#             "social_isolation": 0.00,
#             "coercion": 0.00
#         },

#         active_tactics=[
#             "urgency_pressure",
#             "fear_based_persuasion"
#         ],

#         behavioral_evidence=[
#             {
#                 "turn_id": 2,
#                 "speaker": "Person 2",
#                 "tactic": "urgency_pressure",
#                 "text":
#                     "Yes, I need your help immediately.",
#                 "match_count": 1
#             },
#             {
#                 "turn_id": 4,
#                 "speaker": "Person 2",
#                 "tactic":
#                     "fear_based_persuasion",
#                 "text":
#                     "Your account has been compromised.",
#                 "match_count": 1
#             }
#         ]
#     )

#     engine = BehavioralRiskEngine()

#     result = engine.analyze(
#         state
#     )

#     print()
#     print("=" * 70)
#     print("SAFEConv BEHAVIORAL RISK ENGINE TEST")
#     print("=" * 70)

#     print()

#     print(
#         f"Temporal score    : "
#         f"{result['temporal_score']:.4f}"
#     )

#     print(
#         f"Behavioral score  : "
#         f"{result['behavioral_score']:.4f}"
#     )

#     print(
#         f"Temporal weight   : "
#         f"{result['temporal_weight']:.2f}"
#     )

#     print(
#         f"Behavioral weight : "
#         f"{result['behavioral_weight']:.2f}"
#     )

#     print()

#     print(
#         f"FINAL RISK SCORE  : "
#         f"{result['risk_score']:.4f}"
#     )

#     print(
#         f"RISK LEVEL        : "
#         f"{result['risk_level']}"
#     )

#     print()

#     print(
#         "ACTIVE TACTICS"
#     )

#     for tactic in result[
#         "active_tactics"
#     ]:

#         print(
#             f"  - {tactic}"
#         )

#     print()

#     print(
#         "EVIDENCE"
#     )

#     for evidence in result[
#         "evidence"
#     ]:

#         print(
#             f"\n  Turn {evidence['turn_id']} "
#             f"[{evidence['speaker']}]"
#         )

#         print(
#             f"    Tactic: "
#             f"{evidence['tactic']}"
#         )

#         print(
#             f"    Text: "
#             f"{evidence['text']}"
#         )

#     print()
#     print("=" * 70)

class BehavioralRiskEngine:

    # ========================================================
    # INITIAL ENGINEERING PARAMETERS
    # ========================================================

    TEMPORAL_WEIGHT = 0.70
    BEHAVIORAL_WEIGHT = 0.30

    # These are engineering policy values.
    # They are NOT statistically calibrated thresholds.

    LOW_THRESHOLD = 0.30
    MEDIUM_THRESHOLD = 0.60
    HIGH_THRESHOLD = 0.80

    # Escalation policy
    ESCALATION_THRESHOLD = 0.50

    # ========================================================
    # BEHAVIORAL SCORE
    # ========================================================

    def calculate_behavioral_score(
        self,
        active_tactic_count: int
    ):

        return min(
            active_tactic_count / 8.0,
            1.0
        )

    # ========================================================
    # ESCALATION SCORE
    # ========================================================

    def calculate_escalation(
        self,
        state
    ):

        score = 0.0

        # ----------------------------------------------------
        # 1. Multiple active tactics
        # ----------------------------------------------------

        tactic_count = len(
            state.active_tactics
        )

        if tactic_count >= 2:

            score += 0.25

        elif tactic_count == 1:

            score += 0.10

        # ----------------------------------------------------
        # 2. Behavioral evidence across multiple turns
        # ----------------------------------------------------

        evidence_turns = set()

        for evidence in (
            state.behavioral_evidence
        ):

            evidence_turns.add(
                evidence["turn_id"]
            )

        if len(evidence_turns) >= 3:

            score += 0.25

        elif len(evidence_turns) == 2:

            score += 0.15

        elif len(evidence_turns) == 1:

            score += 0.05

        # ----------------------------------------------------
        # 3. Risk trend
        #
        # Only applied if actual risk history exists.
        # ----------------------------------------------------

        if state.risk_trend == "increasing":

            score += 0.25

        # ----------------------------------------------------
        # 4. High temporal risk
        # ----------------------------------------------------

        if state.temporal_risk >= 0.80:

            score += 0.25

        elif state.temporal_risk >= 0.60:

            score += 0.15

        # ----------------------------------------------------
        # Clamp
        # ----------------------------------------------------

        score = min(
            score,
            1.0
        )

        detected = (
            score >= self.ESCALATION_THRESHOLD
        )

        return {
            "score": score,
            "detected": detected
        }

    # ========================================================
    # RISK LEVEL
    # ========================================================

    def get_risk_level(
        self,
        risk_score: float
    ):

        if risk_score < self.LOW_THRESHOLD:

            return "LOW"

        if risk_score < self.MEDIUM_THRESHOLD:

            return "MEDIUM"

        if risk_score < self.HIGH_THRESHOLD:

            return "HIGH"

        return "CRITICAL"

    # ========================================================
    # MAIN ANALYSIS
    # ========================================================

    def analyze(
        self,
        state
    ):

        # ----------------------------------------------------
        # Behavioral score
        # ----------------------------------------------------

        behavioral_score = (
            self.calculate_behavioral_score(
                len(state.active_tactics)
            )
        )

        # ----------------------------------------------------
        # Temporal score
        # ----------------------------------------------------

        temporal_score = (
            state.temporal_risk
        )

        # ----------------------------------------------------
        # Combined risk
        # ----------------------------------------------------

        risk_score = (

            temporal_score
            * self.TEMPORAL_WEIGHT

        ) + (

            behavioral_score
            * self.BEHAVIORAL_WEIGHT
        )

        risk_score = min(
            max(risk_score, 0.0),
            1.0
        )

        # ----------------------------------------------------
        # Risk level
        # ----------------------------------------------------

        risk_level = self.get_risk_level(
            risk_score
        )

        # ----------------------------------------------------
        # Escalation
        # ----------------------------------------------------

        escalation = (
            self.calculate_escalation(
                state
            )
        )

        state.update_escalation(
            escalation_score=
                escalation["score"],

            escalation_detected=
                escalation["detected"]
        )

        # ----------------------------------------------------
        # Return
        # ----------------------------------------------------

        return {

            "risk_score":
                risk_score,

            "risk_level":
                risk_level,

            "temporal_score":
                temporal_score,

            "behavioral_score":
                behavioral_score,

            "temporal_weight":
                self.TEMPORAL_WEIGHT,

            "behavioral_weight":
                self.BEHAVIORAL_WEIGHT,

            "active_tactics":
                state.active_tactics,

            "active_tactic_count":
                len(state.active_tactics),

            "behavioral_evidence":
                state.behavioral_evidence,

            "escalation_score":
                escalation["score"],

            "escalation_detected":
                escalation["detected"],

            "risk_trend":
                state.risk_trend,

            "risk_delta":
                state.risk_delta
        }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    from safeconv_state import ConversationState

    state = ConversationState()

    state.turn_count = 4
    state.temporal_risk = 0.85

    state.active_tactics = [
        "urgency_pressure",
        "fear_based_persuasion"
    ]

    state.behavioral_evidence = [

        {
            "turn_id": 2,
            "speaker": "Person 2",
            "tactic": "urgency_pressure",
            "text": "Act immediately."
        },

        {
            "turn_id": 4,
            "speaker": "Person 2",
            "tactic": "fear_based_persuasion",
            "text": "Your account is compromised."
        }
    ]

    engine = BehavioralRiskEngine()

    result = engine.analyze(
        state
    )

    print()
    print("=" * 70)
    print("SAFEConv RISK ENGINE TEST")
    print("=" * 70)

    print()

    print(
        f"Temporal score   : "
        f"{result['temporal_score']:.4f}"
    )

    print(
        f"Behavioral score : "
        f"{result['behavioral_score']:.4f}"
    )

    print(
        f"Risk score       : "
        f"{result['risk_score']:.4f}"
    )

    print(
        f"Risk level       : "
        f"{result['risk_level']}"
    )

    print(
        f"Escalation score : "
        f"{result['escalation_score']:.4f}"
    )

    print(
        f"Escalation       : "
        f"{result['escalation_detected']}"
    )

    print(
        f"Risk trend       : "
        f"{result['risk_trend']}"
    )

    print()
    print("=" * 70)