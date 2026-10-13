# import json
# from pathlib import Path


# class SAFEConvRAG:
#     def __init__(self, knowledge_base_path=None):
#         if knowledge_base_path is None:
#             knowledge_base_path = (
#                 Path(__file__).parent
#                 / "knowledge_base"
#                 / "tactics.json"
#             )

#         self.knowledge_base_path = Path(knowledge_base_path)

#         with open(self.knowledge_base_path, "r", encoding="utf-8") as file:
#             data = json.load(file)

#         self.entries = data.get("entries", [])

#         self.tactics = {
#             entry["tactic"]: entry
#             for entry in self.entries
#             if "tactic" in entry
#         }

#         print(f"SAFEConv RAG loaded: {len(self.entries)} entries")

#     def retrieve(self, behavior_result, top_k=5):
#         active_tactics = behavior_result.get("active_tactics", [])
#         evidence = behavior_result.get("evidence", [])

#         # Also collect tactic names present in evidence.
#         evidence_tactics = [
#             item.get("tactic")
#             for item in evidence
#             if item.get("tactic")
#         ]

#         requested_tactics = list(
#             dict.fromkeys(active_tactics + evidence_tactics)
#         )

#         retrieved_entries = []

#         for tactic in requested_tactics:
#             entry = self.tactics.get(tactic)

#             if entry and entry not in retrieved_entries:
#                 retrieved_entries.append(entry)

#             if len(retrieved_entries) >= top_k:
#                 break

#         # Keep only evidence relevant to retrieved tactics.
#         retrieved_tactics = {
#             entry["tactic"] for entry in retrieved_entries
#         }

#         relevant_evidence = [
#             item for item in evidence
#             if item.get("tactic") in retrieved_tactics
#         ]

#         # Build compact context for the LLM.
#         context_parts = []

#         for entry in retrieved_entries:
#             context_parts.append(
#                 f"""
# Tactic: {entry['name']}
# Definition: {entry['definition']}
# Indicators: {", ".join(entry['indicators'])}
# Interpretation: {entry['interpretation']}
# Distinction: {entry['distinction']}
# Recommended actions: {", ".join(entry['recommended_actions'])}
# Knowledge ID: {entry['id']}
# """.strip()
#             )

#         context = "\n\n".join(context_parts)

#         return {
#             "status": "success",
#             "retrieved_ids": [
#                 entry["id"] for entry in retrieved_entries
#             ],
#             "retrieved_tactics": [
#                 entry["tactic"] for entry in retrieved_entries
#             ],
#             "entries": retrieved_entries,
#             "evidence": relevant_evidence,
#             "context": context
#         }

import json
from pathlib import Path

from sentence_transformers import SentenceTransformer


class SAFEConvRAG:
    def __init__(self, knowledge_base_path=None):
        if knowledge_base_path is None:
            knowledge_base_path = (
                Path(__file__).parent
                / "knowledge_base"
                / "tactics.json"
            )

        self.knowledge_base_path = Path(knowledge_base_path)

        with open(self.knowledge_base_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.entries = data.get("entries", [])

        # Semantic embedding model
        self.embedding_model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            device="cpu"
        )

        # Create searchable text for each knowledge entry
        self.entry_texts = [
            self._entry_to_text(entry)
            for entry in self.entries
        ]

        # Precompute knowledge embeddings once at initialization
        self.entry_embeddings = self.embedding_model.encode(
            self.entry_texts,
            convert_to_tensor=True,
            normalize_embeddings=True
        )

        self.tactics = {
            entry["tactic"]: entry
            for entry in self.entries
            if "tactic" in entry
        }

        print(
            f"SAFEConv RAG loaded: {len(self.entries)} entries "
            f"using semantic embeddings"
        )

    @staticmethod
    def _entry_to_text(entry):
        return " ".join([
            entry.get("name", ""),
            entry.get("definition", ""),
            " ".join(entry.get("indicators", [])),
            entry.get("interpretation", ""),
            entry.get("distinction", "")
        ])

    def retrieve(self, behavior_result, top_k=5):
        active_tactics = behavior_result.get("active_tactics", [])
        evidence = behavior_result.get("evidence", [])

        # Use actual message evidence as the primary semantic query.
        evidence_texts = [
            str(item.get("text", "")).strip()
            for item in evidence
            if item.get("text")
        ]

        if evidence_texts:
            query_text = " ".join(evidence_texts)
        else:
            # Fallback when no evidence text is available.
            query_text = " ".join(
                tactic.replace("_", " ")
                for tactic in active_tactics
            )

        if not query_text.strip():
            return {
                "status": "no_query",
                "retrieved_ids": [],
                "retrieved_tactics": [],
                "similarity_scores": [],
                "entries": [],
                "evidence": [],
                "context": ""
            }

        query_embedding = self.embedding_model.encode(
            query_text,
            convert_to_tensor=True,
            normalize_embeddings=True
        )

        # Normalized vectors allow dot product to represent cosine similarity.
        similarities = self.entry_embeddings @ query_embedding

        ranked_indices = similarities.argsort(
            descending=True
        ).tolist()

        retrieved_entries = []
        similarity_scores = []

        for index in ranked_indices:
            entry = self.entries[index]
            score = float(similarities[index].item())

            retrieved_entries.append(entry)
            similarity_scores.append({
                "id": entry["id"],
                "tactic": entry["tactic"],
                "score": round(score, 4)
            })

            if len(retrieved_entries) >= top_k:
                break

        retrieved_tactics = {
            entry["tactic"] for entry in retrieved_entries
        }

        relevant_evidence = [
            item for item in evidence
            if item.get("tactic") in retrieved_tactics
        ]

        context_parts = []

        for entry, score_info in zip(
            retrieved_entries,
            similarity_scores
        ):
            context_parts.append(
                f"""
Tactic: {entry['name']}
Definition: {entry['definition']}
Indicators: {", ".join(entry['indicators'])}
Interpretation: {entry['interpretation']}
Distinction: {entry['distinction']}
Recommended actions: {", ".join(entry['recommended_actions'])}
Similarity score: {score_info['score']}
Knowledge ID: {entry['id']}
""".strip()
            )

        return {
            "status": "success",
            "retrieved_ids": [
                entry["id"] for entry in retrieved_entries
            ],
            "retrieved_tactics": [
                entry["tactic"] for entry in retrieved_entries
            ],
            "similarity_scores": similarity_scores,
            "entries": retrieved_entries,
            "evidence": relevant_evidence,
            "context": "\n\n".join(context_parts)
        }