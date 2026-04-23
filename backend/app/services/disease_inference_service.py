from typing import Dict, List


# ==========================================================
# Disease → Symptoms Mapping (REALISTIC + CLEAN)
# ==========================================================
DISEASE_SYMPTOMS = {
    "malaria": ["fever", "chills", "headache", "fatigue"],
    "dengue": ["fever", "headache", "rash", "joint pain"],
    "cholera": ["diarrhea", "vomiting", "dehydration"],
    "flu": ["fever", "cough", "sore throat", "fatigue"],
    "covid": ["fever", "cough", "fatigue", "shortness of breath", "loss of smell"],
    "tuberculosis": ["cough", "fever", "night sweats", "weight loss"],
    "pneumonia": ["cough", "fever", "shortness of breath", "chest pain"],
    "typhoid": ["fever", "headache", "abdominal pain", "weakness"],
}


# ==========================================================
# 🔥 SIGNATURE SYMPTOMS (HIGH CONFIDENCE SIGNALS)
# ==========================================================
SIGNATURE_SYMPTOMS = {
    "covid": ["loss of smell", "shortness of breath"],
    "flu": ["sore throat"],
    "malaria": ["chills"],
    "dengue": ["joint pain"],
    "cholera": ["dehydration"],
}


# ==========================================================
# WEIGHTS
# ==========================================================
SHARED_WEIGHT = 1.0
SIGNATURE_WEIGHT = 3.0


# ==========================================================
# NORMALIZATION (VERY IMPORTANT)
# ==========================================================
def normalize_symptom(symptom: str) -> str:
    return symptom.strip().lower()


# ==========================================================
# 🔥 CORE FUNCTION
# ==========================================================
def infer_disease_scores(symptom_growth: Dict[str, float]) -> List[Dict]:
    """
    Input:
        {
            "fever": 12.3,
            "cough": 5.2,
            ...
        }

    Output:
        ranked diseases with scores + risk levels
    """

    # Normalize input keys
    normalized_growth = {
        normalize_symptom(k): v for k, v in symptom_growth.items()
    }

    disease_scores = []

    for disease, symptoms in DISEASE_SYMPTOMS.items():
        total = 0.0
        count = 0
        signature_boost = 0.0

        # ---------------------------
        # BASE SYMPTOM SCORING
        # ---------------------------
        for symptom in symptoms:
            symptom = normalize_symptom(symptom)

            if symptom in normalized_growth:
                growth = normalized_growth[symptom]

                # Only consider positive trend
                if growth > 0:
                    total += growth * SHARED_WEIGHT
                    count += 1

        base_score = (total / count) if count > 0 else 0.0

        # ---------------------------
        # SIGNATURE BOOST
        # ---------------------------
        for sig in SIGNATURE_SYMPTOMS.get(disease, []):
            sig = normalize_symptom(sig)

            if sig in normalized_growth:
                growth = normalized_growth[sig]
                if growth > 0:
                    signature_boost += growth * SIGNATURE_WEIGHT

        # ---------------------------
        # FINAL SCORE
        # ---------------------------
        score = base_score + signature_boost

        # ---------------------------
        # 🔥 ANTI-FALSE COVID LOGIC
        # ---------------------------
        if disease == "covid":
            has_signature = any(
                normalize_symptom(s) in normalized_growth and normalized_growth[normalize_symptom(s)] > 0
                for s in SIGNATURE_SYMPTOMS["covid"]
            )

            if not has_signature:
                score *= 0.3  # stronger downgrade

        # ---------------------------
        # RISK LEVEL (IMPROVED)
        # ---------------------------
        if score >= 15:
            risk_level = "HIGH"
        elif score >= 6:
            risk_level = "MEDIUM"
        elif score > 0:
            risk_level = "LOW"
        else:
            risk_level = "NONE"

        disease_scores.append({
            "disease": disease.title(),
            "score": round(score, 2),
            "risk_level": risk_level,
        })

    # Sort descending
    return sorted(disease_scores, key=lambda x: x["score"], reverse=True)