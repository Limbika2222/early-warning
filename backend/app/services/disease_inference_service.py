from typing import Dict, List


# ==========================================================
# Disease → Symptoms Mapping
# ==========================================================
DISEASE_SYMPTOMS = {
    "malaria": ["fever", "chills", "headache", "vomiting", "fatigue"],
    "dengue": ["fever", "headache", "rash", "joint pain", "muscle pain"],
    "cholera": ["diarrhea", "vomiting", "dehydration"],
    "flu": ["fever", "cough", "sore throat", "fatigue", "headache"],
    "covid": ["fever", "cough", "shortness of breath", "fatigue", "loss of smell"],
    "tuberculosis": ["cough", "fever", "night sweats", "weight loss"],
    "pneumonia": ["cough", "fever", "shortness of breath", "chest pain"],
    "measles": ["fever", "rash", "cough", "runny nose"],
    "typhoid": ["fever", "headache", "abdominal pain", "weakness"],
    "hepatitis": ["fatigue", "nausea", "abdominal pain", "jaundice"],
    "food poisoning": ["vomiting", "diarrhea", "abdominal pain", "fever"],
    "meningitis": ["fever", "headache", "stiff neck", "nausea"],
    "ebola": ["fever", "vomiting", "diarrhea", "bleeding"],
    "zika": ["fever", "rash", "joint pain", "red eyes"],
    "chikungunya": ["fever", "joint pain", "muscle pain", "rash"]
}


# ==========================================================
# 🔥 UNIQUE (SIGNATURE) SYMPTOMS
# ==========================================================
SIGNATURE_SYMPTOMS = {
    "covid": ["loss of smell", "shortness of breath"],
    "flu": ["sore throat"],
    "cholera": ["dehydration"],
    "malaria": ["chills"],
}


# ==========================================================
# WEIGHTS
# ==========================================================
SHARED_WEIGHT = 1.0
SIGNATURE_WEIGHT = 3.0   # 🔥 KEY DIFFERENCE


# ==========================================================
# Infer Disease Scores (IMPROVED)
# ==========================================================
def infer_disease_scores(symptom_growth: Dict[str, float]) -> List[Dict]:

    disease_scores = []

    for disease, symptoms in DISEASE_SYMPTOMS.items():
        total = 0
        count = 0
        signature_boost = 0

        for symptom in symptoms:
            if symptom in symptom_growth:
                growth = symptom_growth[symptom]

                if growth > 0:
                    total += growth * SHARED_WEIGHT
                    count += 1

        # 🔥 Check signature symptoms
        signature_list = SIGNATURE_SYMPTOMS.get(disease, [])

        for sig in signature_list:
            if sig in symptom_growth and symptom_growth[sig] > 0:
                signature_boost += symptom_growth[sig] * SIGNATURE_WEIGHT

        # Base score
        base_score = (total / count) if count > 0 else 0

        # 🔥 FINAL SCORE
        score = base_score + signature_boost

        # 🔥 CRITICAL RULE (ANTI-FALSE COVID)
        if disease == "covid":
            has_signature = any(
                s in symptom_growth and symptom_growth[s] > 0
                for s in SIGNATURE_SYMPTOMS["covid"]
            )

            if not has_signature:
                score *= 0.4  # 🔥 heavily downgrade COVID

        # Determine risk level
        if score >= 20:
            risk_level = "HIGH"
        elif score >= 8:
            risk_level = "MEDIUM"
        elif score > 0:
            risk_level = "LOW"
        else:
            risk_level = "NONE"

        disease_scores.append({
            "disease": disease,
            "score": round(score, 2),
            "risk_level": risk_level
        })

    return sorted(disease_scores, key=lambda x: x["score"], reverse=True)