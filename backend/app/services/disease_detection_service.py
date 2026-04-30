from typing import List, Dict
from collections import defaultdict


class DiseaseDetectionService:

    def __init__(self):
        # -----------------------------
        # Disease Knowledge Base
        # -----------------------------
        self.disease_map = {
            "Flu": {
                "fever": 3,
                "cough": 2,
                "fatigue": 2,
                "headache": 1,
            },
            "COVID-like": {
                "fever": 3,
                "cough": 3,
                "fatigue": 2,
                "headache": 1,
            },
            "Malaria": {
                "fever": 3,
                "chills": 3,
                "headache": 2,
                "fatigue": 1,
            },
            "Viral Infection": {
                "fatigue": 3,
                "headache": 2,
                "fever": 1,
            },
        }

    # -----------------------------
    # MAIN FUNCTION
    # -----------------------------
    def detect_diseases(self, time_series: List[Dict]) -> List[Dict]:
        """
        Input: time_series data
        Output: ranked diseases with probabilities (0 → 1)
        """

        # -----------------------------
        # Step 1: Aggregate symptom counts
        # -----------------------------
        symptom_counts = defaultdict(int)

        for item in time_series:
            if item.get("count", 0) > 0:
                symptom = item.get("symptom")
                if symptom:
                    symptom_counts[symptom] += item.get("count", 0)

        # -----------------------------
        # Step 2: Score diseases (FIXED)
        # -----------------------------
        disease_scores = []

        for disease, weights in self.disease_map.items():

            score = 0
            max_score = sum(weights.values())

            for symptom, weight in weights.items():
                if symptom in symptom_counts:
                    # ✅ Normalize contribution (0 → 1 per symptom)
                    presence = min(symptom_counts[symptom] / 3, 1)
                    score += weight * presence

            probability = score / max_score if max_score > 0 else 0

            disease_scores.append({
                "disease": disease,
                "probability": round(probability, 2)
            })

        # -----------------------------
        # Step 3: Sort results
        # -----------------------------
        disease_scores.sort(
            key=lambda x: x["probability"],
            reverse=True
        )

        return disease_scores