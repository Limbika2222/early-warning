import sys
import os

# -------------------------------------------------
# ✅ FIX PATH (KEEP THIS)
# -------------------------------------------------
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -------------------------------------------------
# IMPORTS
# -------------------------------------------------
from app.utils.database import SessionLocal

# ❌ OLD (REMOVE LOGIC DEPENDENCY)
# from app.services.symptom_analysis_service import calculate_symptom_growth
# from app.services.disease_inference_service import infer_disease_scores

# ✅ NEW CORE ANALYSIS
from app.services.risk_scoring_service import (
    compute_disease_risk,
    store_disease_risk,
)

# ✅ KEEP ALERT SYSTEM
from app.services.alert_service import generate_alerts


# -------------------------------------------------
# MAIN PIPELINE
# -------------------------------------------------
def run():
    db = SessionLocal()

    print("🚀 Running full analysis pipeline...\n")

    try:
        # -------------------------------------------------
        # 🔥 STEP 1 — COMPUTE DISEASE RISK (NEW ENGINE)
        # -------------------------------------------------
        disease_risk = compute_disease_risk(db)

        if not disease_risk:
            print("⚠️ No disease risk computed. Stopping pipeline.")
            return

        print("✅ Disease risk calculated (normalized + weighted).")

        # -------------------------------------------------
        # 🔥 STEP 2 — STORE RESULTS
        # -------------------------------------------------
        store_disease_risk(db, disease_risk)
        print("✅ Disease risk stored in database.")

        # -------------------------------------------------
        # 🔥 STEP 3 — GENERATE ALERTS
        # -------------------------------------------------
        alerts = generate_alerts(db, disease_risk)
        print("✅ Alerts generated.\n")

        # -------------------------------------------------
        # OUTPUT ALERTS
        # -------------------------------------------------
        print("🚨 Alerts:")
        if not alerts:
            print("- No alerts triggered")
        else:
            for a in alerts:
                print("-", a["message"])

        print("\n✅ Pipeline completed successfully.")

    except Exception as e:
        print("\n❌ ERROR IN PIPELINE:")
        print(str(e))

    finally:
        db.close()


# -------------------------------------------------
# ENTRY POINT
# -------------------------------------------------
if __name__ == "__main__":
    run()