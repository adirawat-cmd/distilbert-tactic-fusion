# from dataclasses import dataclass, field
# from typing import Dict, List, Optional


# @dataclass
# class ConversationState:
#     """
#     Runtime analytical state maintained by SAFEConv.

#     This is not another machine-learning model.

#     It stores the current understanding of the conversation
#     so that later components such as the Behavioral Risk Engine
#     can reason over the conversation as a whole.
#     """

#     # ========================================================
#     # BASIC CONVERSATION INFORMATION
#     # ========================================================

#     turn_count: int = 0
#     analyzed_turns: int = 0
#     truncated: bool = False

#     # ========================================================
#     # TEMPORAL MODEL INFORMATION
#     # ========================================================

#     temporal_risk: float = 0.0

#     # Risk probability after each analysis/update.
#     risk_history: List[float] = field(
#         default_factory=list
#     )

#     # ========================================================
#     # BEHAVIORAL INFORMATION
#     # ========================================================

#     tactic_scores: Dict[str, float] = field(
#         default_factory=dict
#     )

#     active_tactics: List[str] = field(
#         default_factory=list
#     )

#     behavioral_evidence: List[Dict] = field(
#         default_factory=list
#     )

#     # ========================================================
#     # ESCALATION INFORMATION
#     # ========================================================

#     escalation_score: float = 0.0

#     escalation_detected: bool = False

#     escalation_history: List[float] = field(
#         default_factory=list
#     )

#     # ========================================================
#     # UPDATE TEMPORAL STATE
#     # ========================================================

#     def update_temporal(
#         self,
#         risk_probability: float,
#         turn_count: int,
#         analyzed_turns: int,
#         truncated: bool
#     ):

#         self.temporal_risk = float(
#             risk_probability
#         )

#         self.turn_count = int(
#             turn_count
#         )

#         self.analyzed_turns = int(
#             analyzed_turns
#         )

#         self.truncated = bool(
#             truncated
#         )

#         self.risk_history.append(
#             float(risk_probability)
#         )

#     # ========================================================
#     # UPDATE BEHAVIORAL STATE
#     # ========================================================

#     def update_behavioral(
#         self,
#         tactic_scores: Dict[str, float],
#         active_tactics: Optional[List[str]] = None,
#         behavioral_evidence: Optional[List[Dict]] = None
#     ):

#         self.tactic_scores = dict(
#             tactic_scores
#         )

#         if active_tactics is not None:

#             self.active_tactics = list(
#                 active_tactics
#             )

#         if behavioral_evidence is not None:

#             self.behavioral_evidence = list(
#                 behavioral_evidence
#             )

#     # ========================================================
#     # UPDATE ESCALATION STATE
#     # ========================================================

#     def update_escalation(
#         self,
#         escalation_score: float,
#         escalation_detected: bool
#     ):

#         self.escalation_score = float(
#             escalation_score
#         )

#         self.escalation_detected = bool(
#             escalation_detected
#         )

#         self.escalation_history.append(
#             float(escalation_score)
#         )

#     # ========================================================
#     # RISK TREND
#     # ========================================================

#     @property
#     def risk_trend(self) -> str:

#         if len(self.risk_history) < 2:

#             return "insufficient_history"

#         previous = self.risk_history[-2]
#         current = self.risk_history[-1]

#         difference = current - previous

#         if difference > 0.05:

#             return "increasing"

#         elif difference < -0.05:

#             return "decreasing"

#         else:

#             return "stable"

#     # ========================================================
#     # STATE SUMMARY
#     # ========================================================

#     def summary(self) -> Dict:

#         return {
#             "turn_count": self.turn_count,
#             "analyzed_turns": self.analyzed_turns,
#             "truncated": self.truncated,
#             "temporal_risk": round(
#                 self.temporal_risk,
#                 4
#             ),
#             "risk_trend": self.risk_trend,
#             "risk_history": [
#                 round(value, 4)
#                 for value in self.risk_history
#             ],
#             "tactic_scores": {
#                 key: round(value, 4)
#                 for key, value
#                 in self.tactic_scores.items()
#             },
#             "active_tactics": self.active_tactics,
#             "behavioral_evidence": (
#                 self.behavioral_evidence
#             ),
#             "escalation_score": round(
#                 self.escalation_score,
#                 4
#             ),
#             "escalation_detected": (
#                 self.escalation_detected
#             )
#         }


# # ============================================================
# # TEST
# # ============================================================

# if __name__ == "__main__":

#     state = ConversationState()

#     state.update_temporal(
#         risk_probability=0.8968,
#         turn_count=6,
#         analyzed_turns=6,
#         truncated=False
#     )

#     state.update_behavioral(
#         tactic_scores={
#             "urgency_pressure": 0.8,
#             "fear_based_persuasion": 0.6
#         },
#         active_tactics=[
#             "urgency_pressure",
#             "fear_based_persuasion"
#         ]
#     )

#     state.update_escalation(
#         escalation_score=0.7,
#         escalation_detected=True
#     )

#     print()
#     print("=" * 60)
#     print("SAFEConv Conversation State Test")
#     print("=" * 60)
#     print()

#     print(state.summary())

#     print()
#     print("=" * 60)

class ConversationState:

    def __init__(self):

        # ====================================================
        # Conversation information
        # ====================================================

        self.turn_count = 0
        self.analyzed_turns = 0
        self.truncated = False

        # ====================================================
        # Temporal model
        # ====================================================

        self.temporal_risk = 0.0

        # Risk observations over time.
        #
        # Each entry:
        #
        # {
        #     "turn": ...,
        #     "risk": ...
        # }
        #
        self.risk_history = []

        # ====================================================
        # Behavioral analysis
        # ====================================================

        self.tactic_scores = {}
        self.active_tactics = []
        self.behavioral_evidence = []

        # ====================================================
        # Escalation
        # ====================================================

        self.escalation_score = 0.0
        self.escalation_detected = False
        self.escalation_history = []

    # ========================================================
    # TEMPORAL MODEL UPDATE
    # ========================================================

    def update_temporal(
        self,
        risk_probability: float,
        turn_count: int,
        analyzed_turns: int,
        truncated: bool
    ):

        self.temporal_risk = (
            float(risk_probability)
        )

        self.turn_count = (
            int(turn_count)
        )

        self.analyzed_turns = (
            int(analyzed_turns)
        )

        self.truncated = (
            bool(truncated)
        )

    # ========================================================
    # ADD RISK OBSERVATION
    # ========================================================

    def add_risk_observation(
        self,
        turn: int,
        risk_probability: float
    ):

        observation = {

            "turn":
                int(turn),

            "risk":
                float(risk_probability)
        }

        self.risk_history.append(
            observation
        )

    # ========================================================
    # BEHAVIORAL UPDATE
    # ========================================================

    def update_behavioral(
        self,
        tactic_scores,
        active_tactics,
        behavioral_evidence
    ):

        self.tactic_scores = (
            tactic_scores
        )

        self.active_tactics = (
            active_tactics
        )

        self.behavioral_evidence = (
            behavioral_evidence
        )

    # ========================================================
    # ESCALATION UPDATE
    # ========================================================

    def update_escalation(
        self,
        escalation_score: float,
        escalation_detected: bool
    ):

        self.escalation_score = (
            float(escalation_score)
        )

        self.escalation_detected = (
            bool(escalation_detected)
        )

        self.escalation_history.append(
            {
                "turn":
                    self.turn_count,

                "score":
                    self.escalation_score,

                "detected":
                    self.escalation_detected
            }
        )

    # ========================================================
    # RISK TREND
    # ========================================================

    @property
    def risk_trend(self):

        if len(self.risk_history) < 2:

            return "insufficient_data"

        first_risk = (
            self.risk_history[0]["risk"]
        )

        last_risk = (
            self.risk_history[-1]["risk"]
        )

        delta = (
            last_risk - first_risk
        )

        if delta > 0.05:

            return "increasing"

        if delta < -0.05:

            return "decreasing"

        return "stable"

    # ========================================================
    # RISK DELTA
    # ========================================================

    @property
    def risk_delta(self):

        if len(self.risk_history) < 2:

            return 0.0

        first_risk = (
            self.risk_history[0]["risk"]
        )

        last_risk = (
            self.risk_history[-1]["risk"]
        )

        return (
            last_risk - first_risk
        )

    # ========================================================
    # SUMMARY
    # ========================================================

    def summary(self):

        return {

            "turn_count":
                self.turn_count,

            "analyzed_turns":
                self.analyzed_turns,

            "truncated":
                self.truncated,

            "temporal_risk":
                self.temporal_risk,

            "risk_history":
                self.risk_history,

            "risk_trend":
                self.risk_trend,

            "risk_delta":
                self.risk_delta,

            "tactic_scores":
                self.tactic_scores,

            "active_tactics":
                self.active_tactics,

            "behavioral_evidence":
                self.behavioral_evidence,

            "escalation_score":
                self.escalation_score,

            "escalation_detected":
                self.escalation_detected,

            "escalation_history":
                self.escalation_history
        }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    state = ConversationState()

    # Dummy values only for testing the state mechanism.
    state.add_risk_observation(
        turn=1,
        risk_probability=0.30
    )

    state.add_risk_observation(
        turn=2,
        risk_probability=0.42
    )

    state.add_risk_observation(
        turn=3,
        risk_probability=0.61
    )

    state.add_risk_observation(
        turn=4,
        risk_probability=0.74
    )

    state.turn_count = 4
    state.analyzed_turns = 4

    state.update_escalation(
        escalation_score=0.75,
        escalation_detected=True
    )

    print()
    print("=" * 70)
    print("SAFEConv CONVERSATION STATE TEST")
    print("=" * 70)

    print()

    print(
        "Risk history:"
    )

    for observation in (
        state.risk_history
    ):

        print(
            f"  Turn "
            f"{observation['turn']}: "
            f"{observation['risk']:.2f}"
        )

    print()

    print(
        f"Risk trend : "
        f"{state.risk_trend}"
    )

    print(
        f"Risk delta : "
        f"{state.risk_delta:.2f}"
    )

    print(
        f"Escalation : "
        f"{state.escalation_detected}"
    )

    print()

    print(
        "State summary:"
    )

    print(
        state.summary()
    )

    print()
    print("=" * 70)