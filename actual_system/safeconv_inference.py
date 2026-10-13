# import os
# import json
# import torch
# import torch.nn as nn

# from transformers import AutoTokenizer, AutoModel

# from safeconv_conversation import Conversation


# # ============================================================
# # CONFIGURATION
# # ============================================================

# MODEL_NAME = "distilbert-base-uncased"

# MAX_LENGTH = 128
# MAX_TURNS = 16

# HIDDEN_SIZE = 256
# NUM_LAYERS = 1
# DROPOUT = 0.20

# # Threshold selected from validation data for the
# # trained MentalManip BiLSTM model.
# RISK_THRESHOLD = 0.46

# CHECKPOINT_NAME = "safeconv_distilbert_bilstm_mentalmanip.pt"


# # ============================================================
# # DEVICE
# # ============================================================

# DEVICE = torch.device(
#     "cuda" if torch.cuda.is_available() else "cpu"
# )


# # ============================================================
# # MODEL
# # ============================================================

# class DistilBERTBiLSTM(nn.Module):

#     def __init__(self):
#         super().__init__()

#         self.bert = AutoModel.from_pretrained(MODEL_NAME)

#         self.lstm = nn.LSTM(
#             input_size=768,
#             hidden_size=HIDDEN_SIZE,
#             num_layers=NUM_LAYERS,
#             batch_first=True,
#             bidirectional=True,
#             dropout=DROPOUT if NUM_LAYERS > 1 else 0.0
#         )

#         self.dropout = nn.Dropout(DROPOUT)

#         self.classifier = nn.Linear(
#             HIDDEN_SIZE * 2,
#             2
#         )

#     def forward(
#         self,
#         input_ids,
#         attention_mask,
#         lengths
#     ):

#         batch_size, num_turns, seq_len = input_ids.shape

#         # Flatten turns so DistilBERT processes every
#         # turn independently.
#         input_ids_flat = input_ids.view(
#             batch_size * num_turns,
#             seq_len
#         )

#         attention_mask_flat = attention_mask.view(
#             batch_size * num_turns,
#             seq_len
#         )

#         outputs = self.bert(
#             input_ids=input_ids_flat,
#             attention_mask=attention_mask_flat
#         )

#         # Same representation used during training:
#         # first token embedding.
#         turn_embeddings = outputs.last_hidden_state[:, 0, :]

#         # Restore conversation structure.
#         turn_embeddings = turn_embeddings.view(
#             batch_size,
#             num_turns,
#             768
#         )

#         # Temporal modelling.
#         lstm_output, _ = self.lstm(
#             turn_embeddings
#         )

#         # Create mask so padded turns do not contribute.
#         turn_range = torch.arange(
#             num_turns,
#             device=lengths.device
#         ).unsqueeze(0)

#         turn_mask = (
#             turn_range < lengths.unsqueeze(1)
#         ).float()

#         turn_mask = turn_mask.unsqueeze(-1)

#         # Masked mean across turns.
#         conversation_representation = (
#             (lstm_output * turn_mask).sum(dim=1)
#             / lengths.unsqueeze(1).clamp(min=1)
#         )

#         conversation_representation = self.dropout(
#             conversation_representation
#         )

#         logits = self.classifier(
#             conversation_representation
#         )

#         return logits, conversation_representation


# # ============================================================
# # INFERENCE ENGINE
# # ============================================================

# class SAFEConvInference:

#     def __init__(
#         self,
#         checkpoint_path=None
#     ):

#         if checkpoint_path is None:

#             checkpoint_path = os.path.join(
#                 os.path.dirname(__file__),
#                 CHECKPOINT_NAME
#             )

#         self.checkpoint_path = checkpoint_path

#         print(f"Device: {DEVICE}")
#         print(f"Loading tokenizer: {MODEL_NAME}")

#         self.tokenizer = AutoTokenizer.from_pretrained(
#             MODEL_NAME
#         )

#         print("Loading model...")

#         self.model = DistilBERTBiLSTM()

#         checkpoint = torch.load(
#             self.checkpoint_path,
#             map_location=DEVICE
#         )

#         # Handle either a complete state dictionary
#         # or a checkpoint dictionary.
#         if isinstance(checkpoint, dict):

#             if "model_state_dict" in checkpoint:

#                 state_dict = checkpoint[
#                     "model_state_dict"
#                 ]

#             elif "state_dict" in checkpoint:

#                 state_dict = checkpoint[
#                     "state_dict"
#                 ]

#             else:

#                 state_dict = checkpoint

#         else:

#             state_dict = checkpoint

#         self.model.load_state_dict(
#             state_dict
#         )

#         self.model.to(DEVICE)

#         # IMPORTANT:
#         # This is inference only.
#         self.model.eval()

#         print("Model loaded successfully.")
#         print(f"Checkpoint: {self.checkpoint_path}")
#         print(f"Risk threshold: {RISK_THRESHOLD}")

#     # --------------------------------------------------------
#     # TOKENIZATION
#     # --------------------------------------------------------

#     def tokenize_turns(
#         self,
#         turns
#     ):

#         encoded = self.tokenizer(
#             turns,
#             padding="max_length",
#             truncation=True,
#             max_length=MAX_LENGTH,
#             return_tensors="pt"
#         )

#         return (
#             encoded["input_ids"],
#             encoded["attention_mask"]
#         )

#     # --------------------------------------------------------
#     # PREDICTION
#     # --------------------------------------------------------

#     @torch.no_grad()
#     def predict(
#         self,
#         conversation: Conversation
#     ):

#         if conversation.turn_count == 0:

#             raise ValueError(
#                 "Conversation contains no turns."
#             )

#         # The trained model accepts a maximum of
#         # MAX_TURNS turns.
#         truncated = conversation.turn_count > MAX_TURNS

#         turns = conversation.get_text_turns()[
#             :MAX_TURNS
#         ]

#         actual_turn_count = len(turns)

#         input_ids, attention_mask = (
#             self.tokenize_turns(turns)
#         )

#         # Add batch dimension.
#         input_ids = input_ids.unsqueeze(0)
#         attention_mask = attention_mask.unsqueeze(0)

#         lengths = torch.tensor(
#             [actual_turn_count],
#             dtype=torch.long,
#             device=DEVICE
#         )

#         input_ids = input_ids.to(DEVICE)
#         attention_mask = attention_mask.to(DEVICE)

#         logits, representation = self.model(
#             input_ids=input_ids,
#             attention_mask=attention_mask,
#             lengths=lengths
#         )

#         probabilities = torch.softmax(
#             logits,
#             dim=-1
#         )

#         risk_probability = (
#             probabilities[0, 1].item()
#         )

#         safe_probability = (
#             probabilities[0, 0].item()
#         )

#         risk_label = int(
#             risk_probability >= RISK_THRESHOLD
#         )

#         return {
#             "risk_probability": risk_probability,
#             "safe_probability": safe_probability,
#             "risk_label": risk_label,
#             "threshold": RISK_THRESHOLD,
#             "turn_count": conversation.turn_count,
#             "analyzed_turns": actual_turn_count,
#             "truncated": truncated,
#             "temporal_representation": (
#                 representation[0]
#                 .detach()
#                 .cpu()
#                 .tolist()
#             )
#         }

#     # --------------------------------------------------------
#     # HUMAN-READABLE ANALYSIS
#     # --------------------------------------------------------

#     def analyze(
#         self,
#         conversation: Conversation
#     ):

#         result = self.predict(
#             conversation
#         )

#         if result["risk_label"] == 1:

#             risk_status = "RISK DETECTED"

#         else:

#             risk_status = "NO HIGH RISK DETECTED"

#         result["risk_status"] = risk_status

#         return result


# # ============================================================
# # TEST
# # ============================================================

# if __name__ == "__main__":

#     from safeconv_conversation import (
#         parse_conversation
#     )

#     print()
#     print("=" * 60)
#     print("SAFEConv Runtime Inference Test")
#     print("=" * 60)
#     print()

#     sample_conversation = """
#     Person 1: Hello, I received your message.
#     Person 2: Yes, I need your help immediately.
#     Person 1: What happened?
#     Person 2: Your account has been compromised.
#     Person 1: What should I do?
#     Person 2: Send me the verification code now.
#     """

#     conversation = parse_conversation(
#         sample_conversation
#     )

#     print(
#         f"Conversation turns: "
#         f"{conversation.turn_count}"
#     )

#     print()

#     engine = SAFEConvInference()

#     result = engine.analyze(
#         conversation
#     )

#     print()
#     print("RESULT")
#     print("-" * 60)

#     print(
#         f"Risk probability : "
#         f"{result['risk_probability']:.4f}"
#     )

#     print(
#         f"Safe probability : "
#         f"{result['safe_probability']:.4f}"
#     )

#     print(
#         f"Threshold        : "
#         f"{result['threshold']:.2f}"
#     )

#     print(
#         f"Risk label       : "
#         f"{result['risk_label']}"
#     )

#     print(
#         f"Risk status      : "
#         f"{result['risk_status']}"
#     )

#     print(
#         f"Turns analyzed   : "
#         f"{result['analyzed_turns']}"
#     )

#     print(
#         f"Truncated        : "
#         f"{result['truncated']}"
#     )

#     print(
#         f"Temporal vector  : "
#         f"{len(result['temporal_representation'])}"
#         f" dimensions"
#     )

#     print()
#     print("=" * 60)
import os
import torch
import torch.nn as nn

from transformers import AutoTokenizer, AutoModel

from safeconv_conversation import Conversation


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "distilbert-base-uncased"

MAX_LENGTH = 128
MAX_TURNS = 16

HIDDEN_SIZE = 256
NUM_LAYERS = 1
DROPOUT = 0.20

# Validation-selected threshold for the trained
# MentalManip BiLSTM model.
RISK_THRESHOLD = 0.46

CHECKPOINT_NAME = "safeconv_distilbert_bilstm_mentalmanip.pt"


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ============================================================
# MODEL
# ============================================================

class DistilBERTBiLSTM(nn.Module):

    def __init__(self):
        super().__init__()

        # IMPORTANT:
        # The original training checkpoint uses the name
        # "encoder", not "bert".
        self.encoder = AutoModel.from_pretrained(
            MODEL_NAME
        )

        self.lstm = nn.LSTM(
            input_size=768,
            hidden_size=HIDDEN_SIZE,
            num_layers=NUM_LAYERS,
            batch_first=True,
            bidirectional=True,
            dropout=DROPOUT if NUM_LAYERS > 1 else 0.0
        )

        self.dropout = nn.Dropout(DROPOUT)

        self.classifier = nn.Linear(
            HIDDEN_SIZE * 2,
            2
        )

    def forward(
        self,
        input_ids,
        attention_mask,
        lengths
    ):

        batch_size, num_turns, seq_len = input_ids.shape

        # Flatten all turns so DistilBERT processes
        # each turn independently.
        input_ids_flat = input_ids.view(
            batch_size * num_turns,
            seq_len
        )

        attention_mask_flat = attention_mask.view(
            batch_size * num_turns,
            seq_len
        )

        outputs = self.encoder(
            input_ids=input_ids_flat,
            attention_mask=attention_mask_flat
        )

        # Same turn representation used during training.
        turn_embeddings = outputs.last_hidden_state[:, 0, :]

        # Restore conversation structure.
        turn_embeddings = turn_embeddings.view(
            batch_size,
            num_turns,
            768
        )

        # Temporal modelling.
        lstm_output, _ = self.lstm(
            turn_embeddings
        )

        # Mask padded turns.
        turn_range = torch.arange(
            num_turns,
            device=lengths.device
        ).unsqueeze(0)

        turn_mask = (
            turn_range < lengths.unsqueeze(1)
        ).float()

        turn_mask = turn_mask.unsqueeze(-1)

        # Conversation representation.
        conversation_representation = (
            (lstm_output * turn_mask).sum(dim=1)
            / lengths.unsqueeze(1).clamp(min=1)
        )

        conversation_representation = self.dropout(
            conversation_representation
        )

        logits = self.classifier(
            conversation_representation
        )

        return logits, conversation_representation


# ============================================================
# SAFEConv INFERENCE ENGINE
# ============================================================

class SAFEConvInference:

    def __init__(
        self,
        checkpoint_path=None
    ):

        if checkpoint_path is None:

            checkpoint_path = os.path.join(
                os.path.dirname(__file__),
                CHECKPOINT_NAME
            )

        self.checkpoint_path = checkpoint_path

        print(f"Device: {DEVICE}")
        print(f"Loading tokenizer: {MODEL_NAME}")

        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME
        )

        print("Loading model...")

        self.model = DistilBERTBiLSTM()

        checkpoint = torch.load(
            self.checkpoint_path,
            map_location=DEVICE
        )

        # The training script saved a state dictionary.
        if isinstance(checkpoint, dict):

            if "model_state_dict" in checkpoint:

                state_dict = checkpoint[
                    "model_state_dict"
                ]

            elif "state_dict" in checkpoint:

                state_dict = checkpoint[
                    "state_dict"
                ]

            else:

                state_dict = checkpoint

        else:

            state_dict = checkpoint

        self.model.load_state_dict(
            state_dict
        )

        self.model.to(DEVICE)

        # Inference mode.
        self.model.eval()

        print("Model loaded successfully.")
        print(f"Checkpoint: {self.checkpoint_path}")
        print(
            f"Risk threshold: {RISK_THRESHOLD}"
        )

    # ========================================================
    # TOKENIZATION
    # ========================================================

    def tokenize_turns(self, turns):

        encoded = self.tokenizer(
            turns,
            padding="max_length",
            truncation=True,
            max_length=MAX_LENGTH,
            return_tensors="pt"
        )

        return (
            encoded["input_ids"],
            encoded["attention_mask"]
        )

    # ========================================================
    # PREDICTION
    # ========================================================

    @torch.no_grad()
    def predict(self, conversation: Conversation):

        if conversation.turn_count == 0:

            raise ValueError(
                "Conversation contains no turns."
            )

        # The trained model supports at most 16 turns.
        truncated = (
            conversation.turn_count > MAX_TURNS
        )

        turns = conversation.get_text_turns()[
            :MAX_TURNS
        ]

        actual_turn_count = len(turns)

        input_ids, attention_mask = (
            self.tokenize_turns(turns)
        )

        # Add batch dimension.
        input_ids = input_ids.unsqueeze(0)
        attention_mask = attention_mask.unsqueeze(0)

        lengths = torch.tensor(
            [actual_turn_count],
            dtype=torch.long,
            device=DEVICE
        )

        input_ids = input_ids.to(DEVICE)
        attention_mask = attention_mask.to(DEVICE)

        logits, representation = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            lengths=lengths
        )

        probabilities = torch.softmax(
            logits,
            dim=-1
        )

        safe_probability = (
            probabilities[0, 0].item()
        )

        risk_probability = (
            probabilities[0, 1].item()
        )

        risk_label = int(
            risk_probability >= RISK_THRESHOLD
        )

        return {
            "risk_probability": risk_probability,
            "safe_probability": safe_probability,
            "risk_label": risk_label,
            "threshold": RISK_THRESHOLD,
            "turn_count": conversation.turn_count,
            "analyzed_turns": actual_turn_count,
            "truncated": truncated,
            "temporal_representation": (
                representation[0]
                .detach()
                .cpu()
                .tolist()
            )
        }

    # ========================================================
    # ANALYSIS
    # ========================================================

    def analyze(self, conversation: Conversation):

        result = self.predict(
            conversation
        )

        if result["risk_label"] == 1:

            result["risk_status"] = (
                "RISK DETECTED"
            )

        else:

            result["risk_status"] = (
                "NO HIGH RISK DETECTED"
            )

        return result


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    from safeconv_conversation import (
        parse_conversation
    )

    print()
    print("=" * 60)
    print("SAFEConv Runtime Inference Test")
    print("=" * 60)
    print()

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

    print(
        f"Conversation turns: "
        f"{conversation.turn_count}"
    )

    print()

    engine = SAFEConvInference()

    result = engine.analyze(
        conversation
    )

    print()
    print("RESULT")
    print("-" * 60)

    print(
        f"Risk probability : "
        f"{result['risk_probability']:.4f}"
    )

    print(
        f"Safe probability : "
        f"{result['safe_probability']:.4f}"
    )

    print(
        f"Threshold        : "
        f"{result['threshold']:.2f}"
    )

    print(
        f"Risk label       : "
        f"{result['risk_label']}"
    )

    print(
        f"Risk status      : "
        f"{result['risk_status']}"
    )

    print(
        f"Turns analyzed   : "
        f"{result['analyzed_turns']}"
    )

    print(
        f"Truncated        : "
        f"{result['truncated']}"
    )

    print(
        f"Temporal vector  : "
        f"{len(result['temporal_representation'])}"
        f" dimensions"
    )

    print()
    print("=" * 60)