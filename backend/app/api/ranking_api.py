from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date

from app.utils.database import SessionLocal

from app.services.risk_scoring_service import (
    compute_disease_risk,
)

from app.models.google_trends import (
    Country,
)

# =====================================================
# ROUTER
# =====================================================

router = APIRouter(
    tags=["ranking"]
)

# =====================================================
# DB SESSION
# =====================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# =====================================================
# GET DISEASE RANKING
# =====================================================

@router.get("/diseases")
def get_disease_ranking(

    # -------------------------------------------------
    # 🌍 COUNTRY
    # -------------------------------------------------

    country_iso2: str | None = Query(
        default=None,
        description="ISO2 country code",
    ),

    # -------------------------------------------------
    # 📅 DATE
    # -------------------------------------------------

    date_param: str | None = Query(
        default=None,
        alias="date",
        description=(
            "Preferred date param "
            "(YYYY-MM-DD)"
        ),
    ),

    end_date: str | None = Query(
        default=None,
        description=(
            "Alternative param for "
            "frontend compatibility"
        ),
    ),

    # -------------------------------------------------
    # DB
    # -------------------------------------------------

    db: Session = Depends(get_db),
):
    """
    Returns LIVE computed disease ranking.

    Supports:
    - ?country_iso2=MW
    - ?date=YYYY-MM-DD
    - ?end_date=YYYY-MM-DD
    """

    try:

        # -------------------------------------------------
        # DATE PRIORITY LOGIC
        # -------------------------------------------------

        selected_date_str = (
            date_param or end_date
        )

        analysis_date: date | None = None

        if selected_date_str:

            try:

                analysis_date = (
                    date.fromisoformat(
                        selected_date_str
                    )
                )

            except ValueError:

                print(
                    f"⚠️ Invalid date format: "
                    f"{selected_date_str}"
                )

                return []

        print(
            f"📅 RANKING USING DATE: "
            f"{analysis_date}"
        )

        # -------------------------------------------------
        # COUNTRY LOOKUP
        # -------------------------------------------------

        country_id = None

        country_name = None

        if country_iso2:

            country = (
                db.query(Country)
                .filter(
                    Country.iso2
                    == country_iso2.upper()
                )
                .first()
            )

            if not country:

                print(
                    f"⚠️ Country not found: "
                    f"{country_iso2}"
                )

                return []

            country_id = country.id
            country_name = country.name

        print(
            f"🌍 RANKING COUNTRY: "
            f"{country_name} "
            f"(id={country_id})"
        )

        # -------------------------------------------------
        # COMPUTE RISK
        # -------------------------------------------------

        results = compute_disease_risk(
            db,
            country_id=country_id,
            end_date=analysis_date,
        )

        if not results:

            print(
                "⚠️ No results from "
                "compute_disease_risk"
            )

            return []

        # -------------------------------------------------
        # SORT
        # -------------------------------------------------

        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True,
        )

        # -------------------------------------------------
        # FORMAT RESPONSE
        # -------------------------------------------------

        response = [
            {
                "disease":
                    r.get(
                        "disease",
                        "Unknown",
                    ),

                "risk_score":
                    round(
                        float(
                            r.get(
                                "score",
                                0,
                            )
                        ),
                        3,
                    ),

                "risk_level":
                    r.get(
                        "risk_level",
                        "Unknown",
                    ),

                # 🔥 GEO CONTEXT
                "country_iso2":
                    country_iso2,

                "country_name":
                    country_name,
            }
            for r in results
        ]

        print(
            "🔥 RANKING API RESPONSE:",
            response,
        )

        return response

    except Exception as e:

        print(
            "❌ ERROR in ranking API:",
            str(e),
        )

        return []