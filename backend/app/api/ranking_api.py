from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date

from app.utils.database import SessionLocal
from app.services.risk_scoring_service import compute_disease_risk

router = APIRouter(tags=["ranking"])


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
# 🔥 GET DISEASE RANKING (NOW DATE-AWARE)
# -------------------------------------------------
@router.get("/diseases")
def get_disease_ranking(
    date_param: str | None = Query(
        default=None,
        alias="date",
        description="Date in format YYYY-MM-DD"
    ),
    db: Session = Depends(get_db),
):
    """
    Returns LIVE computed disease ranking
    Supports optional date filtering
    """

    try:
        # -------------------------------------------------
        # 🔥 PARSE DATE
        # -------------------------------------------------
        analysis_date: date | None = None

        if date_param:
            try:
                analysis_date = date.fromisoformat(date_param)
            except ValueError:
                print(f"⚠️ Invalid date format: {date_param}")
                return []

        # -------------------------------------------------
        # 🔥 COMPUTE WITH DATE
        # -------------------------------------------------
        results = compute_disease_risk(
            db,
            end_date=analysis_date
        )

        if not results:
            print("⚠️ No results from compute_disease_risk")
            return []

        # -------------------------------------------------
        # SORT (HIGH → LOW)
        # -------------------------------------------------
        results = sorted(results, key=lambda x: x["score"], reverse=True)

        # -------------------------------------------------
        # FORMAT RESPONSE
        # -------------------------------------------------
        response = [
            {
                "disease": r.get("disease", "Unknown"),
                "risk_score": round(float(r.get("score", 0)), 3),
                "risk_level": r.get("risk_level", "Unknown"),
            }
            for r in results
        ]

        print("🔥 RANKING API RESPONSE:", response)

        return response

    except Exception as e:
        print("❌ ERROR in ranking API:", str(e))
        return []