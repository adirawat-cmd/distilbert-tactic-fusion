

from safeconv_conversation import parse_conversation
from safeconv_inference import SAFEConvInference
from safeconv_state import ConversationState
from safeconv_behavior import analyze_behavior
from safeconv_risk_engine import BehavioralRiskEngine
from safeconv_pii import mask_conversation
from safeconv_llm import SAFEConvLLM
from safeconv_rag import SAFEConvRAG
from safeconv_tactic_features import SAFEConvTacticFeatures

class SAFEConvRuntime:

    def __init__(self):

        print("Initializing SAFEConv runtime...")

       

        self.inference = SAFEConvInference()
        self.llm = SAFEConvLLM()
        self.rag = SAFEConvRAG()
        self.tactic_features = SAFEConvTacticFeatures()
      

        self.risk_engine = BehavioralRiskEngine()

        print("SAFEConv runtime ready.")

    def analyze(
        self,
        conversation_text: str
    ):

     

        conversation = parse_conversation(
            conversation_text
        )

        if conversation.turn_count == 0:

            raise ValueError(
                "No conversation turns could be detected."
            )

       

        pii_result = mask_conversation(
            conversation
        )

        masked_conversation = (
            pii_result["conversation"]
        )

       

        state = ConversationState()

      

        model_result = self.inference.analyze(
            masked_conversation
        )

        state.update_temporal(
            risk_probability=model_result[
                "risk_probability"
            ],
            turn_count=model_result[
                "turn_count"
            ],
            analyzed_turns=model_result[
                "analyzed_turns"
            ],
            truncated=model_result[
                "truncated"
            ]
        )

        

        behavioral_result = analyze_behavior(
            masked_conversation
        )
                # Semantic tactic analysis on the PII-masked conversation
        semantic_text = "\n".join(
            turn.text for turn in masked_conversation.turns
        )

        semantic_tactic_result = (
            self.tactic_features.transform_with_details(
                semantic_text
            )
        )
        print("\nSEMANTIC TACTIC FEATURES:")
        print(semantic_tactic_result)
        state.update_behavioral(
            tactic_scores=behavioral_result[
                "tactic_scores"
            ],
            active_tactics=behavioral_result[
                "active_tactics"
            ],
            behavioral_evidence=behavioral_result[
                "evidence"
            ]
        )

       

        risk_result = self.risk_engine.analyze(
            state
        )
#         llm_result = self.llm.explain(
#     model_result=model_result,
#     behavior_result=behavioral_result,
#     risk_result=risk_result
# )
        rag_result = self.rag.retrieve(
    behavioral_result
)
        llm_result = self.llm.explain(
    model_result=model_result,
    behavior_result=behavioral_result,
    risk_result=risk_result,
    rag_result=rag_result
)
      

        return {

           

            "conversation":
                masked_conversation.to_dict(),

            

            "privacy": {

                "pii_detected":
                    pii_result[
                        "pii_detected"
                    ],

                "detection_count":
                    pii_result[
                        "detection_count"
                    ],

                "pii_types":
                    sorted(
                        set(
                            detection["type"]
                            for detection
                            in pii_result[
                                "detections"
                            ]
                        )
                    )
            },

            

            "model": {

                "risk_probability":
                    model_result[
                        "risk_probability"
                    ],

                "safe_probability":
                    model_result[
                        "safe_probability"
                    ],

                "risk_label":
                    model_result[
                        "risk_label"
                    ],

                "threshold":
                    model_result[
                        "threshold"
                    ],

                "risk_status":
                    model_result[
                        "risk_status"
                    ]
            },

           

            "behavior": {

                "tactic_scores":
                    behavioral_result[
                        "tactic_scores"
                    ],

                "tactic_counts":
                    behavioral_result[
                        "tactic_counts"
                    ],

                "active_tactics":
                    behavioral_result[
                        "active_tactics"
                    ],

                "active_tactic_count":
                    behavioral_result[
                        "active_tactic_count"
                    ],

                "active_tactic_ratio":
                    behavioral_result[
                        "active_tactic_ratio"
                    ],

                "total_matches":
                    behavioral_result[
                        "total_matches"
                    ],

                "evidence":
                    behavioral_result[
                        "evidence"
                    ]
            },
                        "semantic_tactics": semantic_tactic_result,

           

            "state":
                state.summary(),
            "semantic_tactics": semantic_tactic_result,

           

            "risk_assessment":
                risk_result,
            "rag": rag_result,
            "llm_explanation": llm_result
        }




if __name__ == "__main__":

    print()
    
    print("SAFEConv ACTUAL SYSTEM")
   
    print()

    # sample_conversation = """
    # Person 1: Hello, I received your message.
    # Person 2: Yes, I need your help immediately.
    # Person 1: You can contact me at adi@example.com.
    # Person 2: Your account has been compromised.
    # Person 1: My phone number is +91 9876543210.
    # Person 2: Send the verification information to https://example.com/login.
    # """

#     sample_conversation = """
# Person 1: Hello, I received a message saying there is a problem with my account.
# Person 2: Yes, I am from the security department. Your account has been compromised.
# Person 1: What happened?
# Person 2: We detected suspicious activity and you need to act immediately.
# Person 1: What do I need to do?
# Person 2: I need you to verify your identity by sending me the verification code you receive.
# Person 1: Is there another way to verify it?
# Person 2: No. If you do not send the code now, your account may be permanently locked.
# Person 1: Okay, where should I send it?
# Person 2: Send the verification information to https://example.com/login
# """

    sample_conversation = """
Person 1: Hello, I received an email saying there is a problem with my bank account.

Person 2: Hello, I am from the bank security department. We detected suspicious activity on your account.

Person 1: Can you tell me what happened?

Person 2: Someone attempted to access your account from another location. You need to verify your identity immediately.

Person 1: How do I verify it?

Person 2: First, confirm your registered email address and phone number so I can verify that you are the account holder.

Person 1: My email is adi.rawat@example.com and my phone number is +91 9876543210.

Person 2: Thank you. I also need your account number to complete the security verification.

Person 1: My account number is 4587 2391 6642.

Person 2: We have detected another suspicious login. You must complete the verification now.

Person 1: What do I need to do?

Person 2: You will receive a one-time verification code on your phone. Send me that code immediately.

Person 1: I just received the code.

Person 2: Send it to me now. If you do not provide it within five minutes, your account will be temporarily locked.

Person 1: Can I contact the bank directly instead?

Person 2: No, do not contact anyone else. This security case must remain confidential until the investigation is complete.

Person 1: Where should I provide the verification information?

Person 2: Use this secure verification portal: https://secure-bank-example.com/verify/login

Person 1: I am still not sure this is legitimate.

Person 2: If you delay any further, the account will be frozen and you may lose access to your funds.
"""

    runtime = SAFEConvRuntime()

    result = runtime.analyze(
        sample_conversation
    )

    

    print()
    
    print("MASKED CONVERSATION: ")
    

    print(
        f"Turns: "
        f"{result['conversation']['turn_count']}"
    )

    for turn in result[
        "conversation"
    ]["turns"]:

        print(
            f"\nTurn {turn['turn_id']} "
            f"[{turn['speaker']}]"
        )

        print(
            f"  {turn['text']}"
        )

    

    print()
    
    print("PRIVACY PROCESSING: ")
  

    print(
        f"PII detected   : "
        f"{result['privacy']['pii_detected']}"
    )

    print(
        f"PII count      : "
        f"{result['privacy']['detection_count']}"
    )

    print(
        f"PII types      : "
        f"{result['privacy']['pii_types']}"
    )

   

    print()

    print("TEMPORAL MODEL: ")
    

    print(
        f"Risk probability : "
        f"{result['model']['risk_probability']:.4f}"
    )

    print(
        f"Safe probability : "
        f"{result['model']['safe_probability']:.4f}"
    )

    print(
        f"Threshold        : "
        f"{result['model']['threshold']:.2f}"
    )

    print(
        f"Risk label       : "
        f"{result['model']['risk_label']}"
    )

    print(
        f"Risk status      : "
        f"{result['model']['risk_status']}"
    )

    # ========================================================
    # BEHAVIORAL ANALYSIS
    # ========================================================

    print()
    
    print("BEHAVIORAL ANALYSIS: ")
    

    print()

    print("Active tactics:")

    if result["behavior"][
        "active_tactics"
    ]:

        for tactic in result[
            "behavior"
        ]["active_tactics"]:

            print(
                f"  - {tactic}"
            )

    else:

        print("  None")

    print()

    print("Evidence:")

    if result["behavior"][
        "evidence"
    ]:

        for evidence in result[
            "behavior"
        ]["evidence"]:

            print(
                f"\n  Turn {evidence['turn_id']} "
                f"[{evidence['speaker']}]"
            )

            print(
                f"    Tactic: "
                f"{evidence['tactic']}"
            )

            print(
                f"    Text: "
                f"{evidence['text']}"
            )

    else:

        print("  None")

   

    assessment = result[
        "risk_assessment"
    ]

    print()
    print("FINAL SAFEConv RISK ASSESSMENT")

    print()

    print(
        f"Temporal score    : "
        f"{assessment['temporal_score']:.4f}"
    )

    print(
        f"Behavioral score  : "
        f"{assessment['behavioral_score']:.4f}"
    )

    print(
        f"Temporal weight   : "
        f"{assessment['temporal_weight']:.2f}"
    )

    print(
        f"Behavioral weight : "
        f"{assessment['behavioral_weight']:.2f}"
    )

    print()

    print(
        f"FINAL RISK SCORE  : "
        f"{assessment['risk_score']:.4f}"
    )

    print(
        f"RISK LEVEL        : "
        f"{assessment['risk_level']}"
    )

    print()

    print(
        f"Escalation score  : "
        f"{assessment['escalation_score']:.4f}"
    )

    print(
        f"Escalation        : "
        f"{assessment['escalation_detected']}"
    )

    print(
        f"Risk trend        : "
        f"{assessment['risk_trend']}"
    )

    print(
        f"Risk delta        : "
        f"{assessment['risk_delta']:.4f}"
    )
    rag_result = result["rag"]
    print()
    print("RAG STATUS:", rag_result.get("status"))
    print("RAG RETRIEVED:", rag_result.get("retrieved_tactics"))
    print("RAG SCORES:", rag_result.get("similarity_scores"))
    print()
    print(f"LLM: {result["llm_explanation"]}")
    print()
    print()
    print("-" * 70)
    print("SAFEConv ANALYSIS COMPLETE")
 