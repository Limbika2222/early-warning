from fastapi import APIRouter

from sqlalchemy.orm import Session

from app.utils.database import (
    SessionLocal,
)

from app.services.prediction.feature_builder import (
    build_prediction_features,
)

from app.services.prediction.disease_mapper import (
    infer_disease_scores,
)

from app.services.prediction.seasonality_service import (
    analyze_seasonality,
)


router = APIRouter(

    prefix="/api/predictions",

    tags=["Predictions"],
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
# LIVE PREDICTIONS
# =====================================================

@router.get("/live")
def get_live_predictions():

    db: Session = SessionLocal()

    try:

        # -------------------------------------------------
        # RAW FEATURES
        # -------------------------------------------------

        raw_predictions = (
            build_prediction_features(
                db
            )
        )

        # -------------------------------------------------
        # DISEASE INFERENCE
        # -------------------------------------------------

        inferred_predictions = (
            infer_disease_scores(
                raw_predictions
            )
        )

        return {

            "source":
                "Prediction Engine",

            "count":
                len(
                    inferred_predictions
                ),

            "predictions":
                inferred_predictions,
        }

    except Exception as e:

        print(
            "❌ Prediction API error:",
            str(e)
        )

        return {

            "source":
                "Prediction Engine",

            "count":
                0,

            "predictions":
                [],
        }

    finally:

        db.close()

# =====================================================
# COUNTRY-AWARE SEASONALITY
# =====================================================

from app.services.prediction.country_seasonality import (
    COUNTRY_SEASONALITY,
)

@router.get("/seasonality")
def get_seasonality():

    results = []

    for country, diseases in COUNTRY_SEASONALITY.items():

        for disease, data in diseases.items():

            results.append({

                "country": country,

                "disease": disease,

                "peak_month": data["peak_month"],

                "top_months": data["top_months"],

                "seasonality_strength":
                    data["seasonality_strength"],

                "seasonal_risk":
                    (
                        "HIGH"
                        if data["seasonality_strength"] >= 0.8
                        else "MEDIUM"
                    ),
            })

    return {
        "source": "Geo-Aware Seasonality Engine",
        "count": len(results),
        "results": results,
    }

# =====================================================
# TOP HIGH-RISK DISEASES
# =====================================================

@router.get("/high-risk")
def get_high_risk_predictions():

    db: Session = SessionLocal()

    try:

        raw_predictions = (
            build_prediction_features(
                db
            )
        )

        inferred_predictions = (
            infer_disease_scores(
                raw_predictions
            )
        )

        high_risk = [

            item

            for item in (
                inferred_predictions
            )

            if item[
                "risk_level"
            ] == "HIGH"
        ]

        return {

            "source":
                "Prediction Engine",

            "count":
                len(high_risk),

            "predictions":
                high_risk,
        }

    except Exception as e:

        print(
            "❌ High-risk API error:",
            str(e)
        )

        return {

            "source":
                "Prediction Engine",

            "count":
                0,

            "predictions":
                [],
        }

    finally:

        db.close()


# =====================================================
# SINGLE DISEASE PREDICTION
# =====================================================

@router.get("/disease/{disease_name}")
def get_prediction_by_disease(
    disease_name: str
):

    db: Session = SessionLocal()

    try:

        raw_predictions = (
            build_prediction_features(
                db
            )
        )

        inferred_predictions = (
            infer_disease_scores(
                raw_predictions
            )
        )

        filtered = [

            item

            for item in (
                inferred_predictions
            )

            if item[
                "disease"
            ].lower() == (
                disease_name.lower()
            )
        ]

        return {

            "source":
                "Prediction Engine",

            "count":
                len(filtered),

            "predictions":
                filtered,
        }

    except Exception as e:

        print(
            "❌ Disease prediction error:",
            str(e)
        )

        return {

            "source":
                "Prediction Engine",

            "count":
                0,

            "predictions":
                [],
        }

    finally:

        db.close()
