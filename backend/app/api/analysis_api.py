from fastapi import APIRouter
import subprocess
import sys
import os

from app.services.risk_scoring_service import compute_disease_risk
from app.utils.database import SessionLocal

router = APIRouter()


# -------------------------------------------------
# 🔥 HELPER → Explain disease (VERY IMPORTANT)
# -------------------------------------------------
def generate_disease_explanation(disease_name: str):
    explanations = {
        "COVID-19": "Multiple respiratory symptoms like cough, fatigue, and shortness of breath are trending.",
        "Influenza": "Common flu symptoms such as fever, fatigue, and chills are increasing.",
        "Malaria": "Symptoms like fever, chills, and headache indicate possible malaria spread.",
        "Dengue": "High fever with joint and muscle pain suggests dengue activity.",
        "Typhoid": "Fever and abdominal pain trends indicate possible typhoid cases.",
        "Pneumonia": "Respiratory symptoms like cough and chest pain are rising.",
        "Tuberculosis": "Chronic cough and weight loss signals TB patterns.",
        "Asthma": "Breathing difficulty and chest tightness trends detected.",
        "Common Cold": "Mild symptoms like runny nose and sneezing increasing.",
        "Food Poisoning": "Nausea and abdominal symptoms trending.",
        "Migraine": "Headache-related searches increasing significantly.",
    }

    return explanations.get(
        disease_name,
        "Symptom patterns indicate increased activity for this disease."
    )


# -------------------------------------------------
# 🔥 RUN ANALYSIS + RETURN SMART CLASSIFICATION
# -------------------------------------------------
@router.post("/run")
def run_analysis():
    db = SessionLocal()

    try:
        # -------------------------------------------------
        # 1. RUN YOUR EXISTING PIPELINE (OPTIONAL)
        # -------------------------------------------------
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        script_path = os.path.join(base_dir, "scripts", "run_full_analysis.py")

        print(f"🚀 Running analysis script: {script_path}")

        subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
        )

        # -------------------------------------------------
        # 2. GET DISEASE RANKING (🔥 IMPORTANT)
        # -------------------------------------------------
        results = compute_disease_risk(db)

        if not results:
            return {
                "status": "success",
                "classification": "No significant disease detected",
                "risk_level": "LOW",
                "explanation": "No strong symptom signals found.",
                "top_disease": None,
                "ranking": [],
            }

        # -------------------------------------------------
        # 3. GET TOP DISEASE
        # -------------------------------------------------
        top = results[0]

        explanation = generate_disease_explanation(top["disease"])

        # -------------------------------------------------
        # 4. RETURN SMART RESPONSE
        # -------------------------------------------------
        return {
            "status": "success",

            # 🔥 THIS REPLACES "Influenza-like Illness"
            "classification": top["disease"],

            "risk_level": top["risk_level"],

            # 🔥 NEW (very important for UI)
            "explanation": explanation,

            # 🔥 EXTRA DATA
            "top_disease": top,
            "ranking": results,
        }

    except Exception as e:
        print(f"❌ Error in analysis: {e}")

        return {
            "status": "error",
            "message": str(e),
        }

    finally:
        db.close()