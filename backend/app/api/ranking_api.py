from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.utils.database import SessionLocal

# ✅ NEW ENGINE
from app.services.risk_scoring_service import compute_disease_risk

router = APIRouter(prefix="/api/ranking", tags=["ranking"])


# -------------------------------------------------
# DB SESSION
# -------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------------
# 🔥 GET DISEASE RANKING (NEW LOGIC)
# -------------------------------------------------
@router.get("/diseases")
def get_disease_ranking(db: Session = Depends(get_db)):
    """
    Returns LIVE computed disease ranking using:
    - multi-upload data
    - normalization
    - weighted scoring
    """

    # -------------------------------------------------
    # 🔥 STEP 1: COMPUTE (NO DB DEPENDENCY)
    # -------------------------------------------------
    results = compute_disease_risk(db)

    if not results:
        print("⚠️ No results from compute_disease_risk")
        return []

    # -------------------------------------------------
    # 🔥 STEP 2: SORT (HIGH → LOW)
    # -------------------------------------------------
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    # -------------------------------------------------
    # 🔥 STEP 3: FORMAT RESPONSE
    # -------------------------------------------------
    response = [
        {
            "disease": r["disease"],
            "risk_score": round(float(r["score"]), 3),  # ✅ clean output
            "risk_level": r["risk_level"],
        }
        for r in results
    ]

    # -------------------------------------------------
    # DEBUG LOG
    # -------------------------------------------------
    print("🔥 RANKING API RESPONSE (NEW ENGINE):", response)

    return response