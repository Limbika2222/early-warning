from fastapi import (
    APIRouter,
    Query,
)

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

from app.services.prediction.country_seasonality import (
    COUNTRY_SEASONALITY,
)

router = APIRouter(

    prefix="/api/predictions",

    tags=["Predictions"],
)

# =====================================================
# COUNTRY NORMALIZATION
# =====================================================

COUNTRY_ALIASES = {

    "India": "IN",
    "Malawi": "MW",
    "South Africa": "ZA",
    "United States": "US",
    "Kenya": "KE",
    "Nigeria": "NG",
    "Tanzania": "TZ",
    "Uganda": "UG",
    "Ethiopia": "ET",

    # ISO passthrough
    "IN": "IN",
    "MW": "MW",
    "ZA": "ZA",
    "US": "US",
    "KE": "KE",
    "NG": "NG",
    "TZ": "TZ",
    "UG": "UG",
    "ET": "ET",

    "GLOBAL": "GLOBAL",
}

# =====================================================
# NORMALIZE COUNTRY
# =====================================================

def normalize_country(
    value
):

    if not value:
        return "GLOBAL"

    value = str(value).strip()

    return COUNTRY_ALIASES.get(
        value,
        value
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
# COUNTRY-AWARE
# =====================================================

@router.get("/live")
def get_live_predictions(

    country: str = Query(
        default="GLOBAL"
    )

):

    db: Session = SessionLocal()

    try:

        # -------------------------------------------------
        # NORMALIZE COUNTRY
        # -------------------------------------------------

        country = normalize_country(
            country
        )

        # -------------------------------------------------
        # BUILD FEATURES
        # -------------------------------------------------

        raw_predictions = (
            build_prediction_features(
                db
            )
        )

        # -------------------------------------------------
        # INFER SCORES
        # -------------------------------------------------

        inferred_predictions = (
            infer_disease_scores(
                raw_predictions
            )
        )

        # -------------------------------------------------
        # NORMALIZE PREDICTION COUNTRIES
        # -------------------------------------------------

        for item in inferred_predictions:

            item["country"] = (
                normalize_country(

                    item.get(
                        "country",
                        "GLOBAL",
                    )
                )
            )

        # -------------------------------------------------
        # COUNTRY FILTER
        # -------------------------------------------------

        if country != "GLOBAL":

            inferred_predictions = [

                item

                for item in (
                    inferred_predictions
                )

                if (
                    item.get(
                        "country"
                    ) == country
                )
            ]

        # -------------------------------------------------
        # REMOVE EMPTY SIGNALS
        # -------------------------------------------------

        inferred_predictions = [

            item

            for item in (
                inferred_predictions
            )

            if item.get(
                "combined_score",
                0
            ) > 0
        ]

        # -------------------------------------------------
        # SORT
        # -------------------------------------------------

        inferred_predictions = sorted(

            inferred_predictions,

            key=lambda x:
            x["combined_score"],

            reverse=True,
        )

        return {

            "source":
                "Geo-Aware Prediction Engine",

            "country":
                country,

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
                "Geo-Aware Prediction Engine",

            "country":
                country,

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

@router.get("/seasonality")
def get_seasonality(

    country: str = Query(
        default="GLOBAL"
    )

):

    country = normalize_country(
        country
    )

    results = []

    # -------------------------------------------------
    # GLOBAL MODE
    # -------------------------------------------------

    if country == "GLOBAL":

        for (
            country_code,
            diseases
        ) in COUNTRY_SEASONALITY.items():

            for (
                disease,
                data
            ) in diseases.items():

                results.append({

                    "country":
                        country_code,

                    "disease":
                        disease,

                    "peak_month":
                        data["peak_month"],

                    "top_months":
                        data["top_months"],

                    "seasonality_strength":
                        data[
                            "seasonality_strength"
                        ],

                    "seasonal_risk":
                        (
                            "HIGH"
                            if data[
                                "seasonality_strength"
                            ] >= 0.8
                            else "MEDIUM"
                        ),
                })

    # -------------------------------------------------
    # COUNTRY FILTER MODE
    # -------------------------------------------------

    else:

        country_data = (

            COUNTRY_SEASONALITY.get(
                country,
                {}
            )
        )

        for (
            disease,
            data
        ) in country_data.items():

            results.append({

                "country":
                    country,

                "disease":
                    disease,

                "peak_month":
                    data["peak_month"],

                "top_months":
                    data["top_months"],

                "seasonality_strength":
                    data[
                        "seasonality_strength"
                    ],

                "seasonal_risk":
                    (
                        "HIGH"
                        if data[
                            "seasonality_strength"
                        ] >= 0.8
                        else "MEDIUM"
                    ),
            })

    return {

        "source":
            "Geo-Aware Seasonality Engine",

        "country":
            country,

        "count":
            len(results),

        "results":
            results,
    }

# =====================================================
# HIGH-RISK PREDICTIONS
# =====================================================

@router.get("/high-risk")
def get_high_risk_predictions(

    country: str = Query(
        default="GLOBAL"
    )

):

    db: Session = SessionLocal()

    try:

        country = normalize_country(
            country
        )

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

        # -------------------------------------------------
        # NORMALIZE COUNTRIES
        # -------------------------------------------------

        for item in inferred_predictions:

            item["country"] = (
                normalize_country(

                    item.get(
                        "country",
                        "GLOBAL",
                    )
                )
            )

        # -------------------------------------------------
        # COUNTRY FILTER
        # -------------------------------------------------

        if country != "GLOBAL":

            inferred_predictions = [

                item

                for item in (
                    inferred_predictions
                )

                if (
                    item.get(
                        "country"
                    ) == country
                )
            ]

        # -------------------------------------------------
        # HIGH RISK ONLY
        # -------------------------------------------------

        high_risk = [

            item

            for item in (
                inferred_predictions
            )

            if item[
                "risk_level"
            ] == "HIGH"
        ]

        # -------------------------------------------------
        # SORT
        # -------------------------------------------------

        high_risk = sorted(

            high_risk,

            key=lambda x:
            x["combined_score"],

            reverse=True,
        )

        return {

            "source":
                "Geo-Aware Prediction Engine",

            "country":
                country,

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
                "Geo-Aware Prediction Engine",

            "country":
                country,

            "count":
                0,

            "predictions":
                [],
        }

    finally:

        db.close()

# =====================================================
# SINGLE DISEASE
# =====================================================

@router.get("/disease/{disease_name}")
def get_prediction_by_disease(

    disease_name: str,

    country: str = Query(
        default="GLOBAL"
    )

):

    db: Session = SessionLocal()

    try:

        country = normalize_country(
            country
        )

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

        # -------------------------------------------------
        # NORMALIZE COUNTRIES
        # -------------------------------------------------

        for item in inferred_predictions:

            item["country"] = (
                normalize_country(

                    item.get(
                        "country",
                        "GLOBAL",
                    )
                )
            )

        # -------------------------------------------------
        # COUNTRY FILTER
        # -------------------------------------------------

        if country != "GLOBAL":

            inferred_predictions = [

                item

                for item in (
                    inferred_predictions
                )

                if (
                    item.get(
                        "country"
                    ) == country
                )
            ]

        # -------------------------------------------------
        # DISEASE FILTER
        # -------------------------------------------------

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

        # -------------------------------------------------
        # SORT
        # -------------------------------------------------

        filtered = sorted(

            filtered,

            key=lambda x:
            x["combined_score"],

            reverse=True,
        )

        return {

            "source":
                "Geo-Aware Prediction Engine",

            "country":
                country,

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
                "Geo-Aware Prediction Engine",

            "country":
                country,

            "count":
                0,

            "predictions":
                [],
        }

    finally:

        db.close()