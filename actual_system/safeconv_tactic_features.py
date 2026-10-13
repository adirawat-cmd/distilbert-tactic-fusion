
import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SAFEConvTacticFeatures:
    TACTIC_ORDER = [
        "urgency_pressure",
        "fear_based_persuasion",
        "impersonation",
        "emotional_manipulation",
        "financial_extraction",
        "trust_engineering",
        "social_isolation",
        "coercion",
    ]

    def __init__(
        self,
        knowledge_base_path=None,
        model_name="all-MiniLM-L6-v2",
    ):
        if knowledge_base_path is None:
            knowledge_base_path = (
                Path(__file__).parent
                / "knowledge_base"
                / "tactics.json"
            )

        self.knowledge_base_path = Path(knowledge_base_path)

        # Load the tactic knowledge base.
        with self.knowledge_base_path.open(
            "r", encoding="utf-8"
        ) as file:
            data = json.load(file)

        # Your tactics.json stores the eight tactics under "entries".
        if isinstance(data, dict):
            entries = data.get(
                "entries",
                data.get("tactics", []),
            )
        elif isinstance(data, list):
            entries = data
        else:
            raise ValueError(
                "Invalid knowledge base format."
            )

        # Also support knowledge bases stored as dictionaries.
        if isinstance(entries, dict):
            normalized_entries = []

            for key, value in entries.items():
                if isinstance(value, dict):
                    entry = dict(value)
                    entry.setdefault("tactic", key)
                    normalized_entries.append(entry)

            entries = normalized_entries

        # Index entries by their canonical tactic names.
        self.tactics = {}

        for entry in entries:
            tactic = entry.get("tactic")

            if tactic in self.TACTIC_ORDER:
                self.tactics[tactic] = entry

        missing = [
            tactic
            for tactic in self.TACTIC_ORDER
            if tactic not in self.tactics
        ]

        if missing:
            raise ValueError(
                "Knowledge base is missing tactics: "
                f"{missing}"
            )

        # Load Sentence-BERT.
        self.encoder = SentenceTransformer(model_name)

        # Generate one semantic embedding per tactic.
        self.tactic_embeddings = {}

        for tactic in self.TACTIC_ORDER:
            entry = self.tactics[tactic]

            indicators = entry.get("indicators", [])
            if isinstance(indicators, list):
                indicators = " ".join(
                    str(item) for item in indicators
                )

            descriptions = [
                entry.get("name", tactic),
                entry.get("definition", ""),
                indicators,
                entry.get("example", ""),
                entry.get("interpretation", ""),
                entry.get("distinction", ""),
            ]

            tactic_text = " ".join(
                str(item).strip()
                for item in descriptions
                if item
            )

            embedding = self.encoder.encode(
                [tactic_text],
                normalize_embeddings=True,
                convert_to_numpy=True,
            )[0]

            self.tactic_embeddings[tactic] = embedding

        # Stack embeddings in a consistent order.
        self.tactic_matrix = np.stack(
            [
                self.tactic_embeddings[tactic]
                for tactic in self.TACTIC_ORDER
            ]
        )

        print(
            "SAFEConv tactic feature extractor initialized."
        )
        print(f"Tactics loaded: {len(self.tactics)}")
        print(f"Embedding model: {model_name}")

    def transform(self, conversation_text):
        """
        Convert a conversation into an 8-dimensional
        semantic tactic feature vector.

        Each feature is the cosine similarity between the
        conversation embedding and one tactic embedding.
        """
        if not isinstance(conversation_text, str):
            raise TypeError(
                "conversation_text must be a string."
            )

        if not conversation_text.strip():
            return np.zeros(
                len(self.TACTIC_ORDER),
                dtype=np.float32,
            )

        conversation_embedding = self.encoder.encode(
            [conversation_text],
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        similarities = cosine_similarity(
            conversation_embedding,
            self.tactic_matrix,
        )[0]

        return similarities.astype(np.float32)

    def transform_with_details(self, conversation_text):
        """Return features together with their tactic names."""
        features = self.transform(conversation_text)

        return {
            "tactic_order": list(self.TACTIC_ORDER),
            "features": features.tolist(),
            "dimensions": int(features.shape[0]),
        }


if __name__ == "__main__":
    extractor = SAFEConvTacticFeatures()

    sample = (
        "Your bank account will be blocked in five minutes. "
        "Send me your verification code immediately and "
        "do not contact anyone else."
    )

    result = extractor.transform_with_details(sample)

    print("\nSample conversation:")
    print(sample)

    print("\nTactic feature vector:")
    for tactic, score in zip(
        result["tactic_order"],
        result["features"],
    ):
        print(f"{tactic}: {score:.4f}")

    print("\nDimensions:", result["dimensions"])
    print("Feature vector:", result["features"])
