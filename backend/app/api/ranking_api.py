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
# 🔥 GET DISEASE RANKING (DATE-AWARE FIXED)
# -------------------------------------------------
@router.get("/diseases")
def get_disease_ranking(
    date_param: str | None = Query(
        default=None,
        alias="date",
        description="Preferred date param (YYYY-MM-DD)"
    ),
    end_date: str | None = Query(
        default=None,
        description="Alternative param for frontend compatibility"
    ),
    db: Session = Depends(get_db),
):
    """
    Returns LIVE computed disease ranking
    Supports:
    - ?date=YYYY-MM-DD
    - ?end_date=YYYY-MM-DD
    """

    try:
        # -------------------------------------------------
        # 🔥 PICK DATE (PRIORITY LOGIC)
        # -------------------------------------------------
        selected_date_str = date_param or end_date

        analysis_date: date | None = None

        if selected_date_str:
            try:
                analysis_date = date.fromisoformat(selected_date_str)
            except ValueError:
                print(f"⚠️ Invalid date format: {selected_date_str}")
                return []

        print(f"📅 RANKING USING DATE: {analysis_date}")

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
        # SORT
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