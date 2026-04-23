import re
from typing import Dict, List


# ==========================================================
# 🔥 BASE SYMPTOM MAP (EXPANDABLE)
# ==========================================================
SYMPTOM_MAP: Dict[str, List[str]] = {
    "fever": ["fever", "high fever", "mild fever"],
    "cough": ["cough", "dry cough", "severe cough"],
    "fatigue": ["fatigue", "tiredness", "weakness"],
    "headache": ["headache", "severe headache", "migraine"],
    "chills": ["chills", "cold chills"],
    "sore throat": ["sore throat", "throat pain"],
    "shortness of breath": ["shortness of breath", "breathing difficulty"],
    "nausea": ["nausea", "feeling nauseous"],
    "vomiting": ["vomiting", "throwing up"],
    "diarrhea": ["diarrhea", "loose stool"],
    "rash": ["rash", "skin rash"],
    "joint pain": ["joint pain", "body pain"],
    "muscle pain": ["muscle pain", "body ache"],
    "abdominal pain": ["abdominal pain", "stomach pain"],
    "runny nose": ["runny nose", "nasal congestion"],
}


# ==========================================================
# 🔥 CLEAN RAW KEYWORD
# ==========================================================
def clean_keyword(keyword: str) -> str:
    if not keyword:
        return ""

    keyword = keyword.lower().strip()

    # remove ".1", ".2", etc
    keyword = re.sub(r"\.\d+$", "", keyword)

    # remove special chars
    keyword = re.sub(r"[^a-z\s]", " ", keyword)

    # normalize spaces
    keyword = re.sub(r"\s+", " ", keyword)

    return keyword.strip()


# ==========================================================
# 🔥 NORMALIZE TO BASE SYMPTOM
# ==========================================================
def normalize_symptom(keyword: str) -> str:
    """
    Convert raw keyword → standardized symptom

    Example:
    "fatigue.1" → "fatigue"
    "severe headache" → "headache"
    """

    keyword = clean_keyword(keyword)

    for base, variants in SYMPTOM_MAP.items():
        for variant in variants:
            if variant in keyword:
                return base

    # fallback → return cleaned keyword
    return keyword


# ==========================================================
# 🔥 BULK NORMALIZATION
# ==========================================================
def normalize_symptom_list(keywords: List[str]) -> List[str]:
    return [normalize_symptom(k) for k in keywords]


# ==========================================================
# 🔥 GROUP SIMILAR SYMPTOMS
# ==========================================================
def group_symptoms(symptom_values: Dict[str, float]) -> Dict[str, float]:
    """
    Merge duplicate/similar symptoms into one.

    Example:
    {"fatigue": 10, "fatigue.1": 5} → {"fatigue": 15}
    """

    grouped: Dict[str, float] = {}

    for raw_symptom, value in symptom_values.items():
        normalized = normalize_symptom(raw_symptom)

        if normalized not in grouped:
            grouped[normalized] = 0

        grouped[normalized] += value

    return grouped


# ==========================================================
# 🔥 DEBUG HELPER
# ==========================================================
def debug_normalization(samples: List[str]):
    print("\n🔍 NORMALIZATION DEBUG")
    for s in samples:
        print(f"{s} → {normalize_symptom(s)}")