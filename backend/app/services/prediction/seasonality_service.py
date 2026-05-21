from collections import defaultdict
from calendar import month_name

from sqlalchemy.orm import Session

from app.models.google_trends import (
    GoogleTrendsTimeseries,
)

from app.services.prediction.disease_mapper import (
    map_keyword_to_disease,
)

# =====================================================
# MONTH NAMES
# =====================================================

MONTHS = {

    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}

# =====================================================
# ANALYZE SEASONALITY
# =====================================================

def analyze_seasonality(
    db: Session
):

    print(
        "📅 Running seasonality analysis..."
    )

    # =================================================
    # FETCH DATA
    # =================================================

    rows = (
        db.query(
            GoogleTrendsTimeseries
        )
        .all()
    )

    # =================================================
    # STORAGE
    # =================================================

    disease_month_scores = defaultdict(

        lambda: defaultdict(float)
    )

    # =================================================
    # PROCESS
    # =================================================

    for row in rows:

        # ---------------------------------------------
        # KEYWORD
        # ---------------------------------------------

        if not row.keyword:
            continue

        keyword = (
            row.keyword.keyword_text
        )

        disease = (
            map_keyword_to_disease(
                keyword
            )
        )

        if disease == "Unknown":
            continue

        # ---------------------------------------------
        # MONTH
        # ---------------------------------------------

        if not row.date:
            continue

        month = row.date.month

        # ---------------------------------------------
        # SCORE
        # ---------------------------------------------

        score = (
            row.interest_index or 0
        )

        disease_month_scores[
            disease
        ][month] += score

    # =================================================
    # BUILD RESULTS
    # =================================================

    results = []

    for disease, months in (
        disease_month_scores.items()
    ):

        if not months:
            continue

        # ---------------------------------------------
        # PEAK MONTH
        # ---------------------------------------------

        peak_month_num = max(
            months,
            key=months.get
        )

        peak_score = months[
            peak_month_num
        ]

        # ---------------------------------------------
        # SORT MONTHS
        # ---------------------------------------------

        sorted_months = sorted(

            months.items(),

            key=lambda x: x[1],

            reverse=True,
        )

        top_months = [

            MONTHS[m[0]]

            for m in sorted_months[:3]
        ]

        # ---------------------------------------------
        # SEASONALITY STRENGTH
        # ---------------------------------------------

        total = sum(
            months.values()
        )

        strength = round(

            peak_score / total,

            2,
        )

        # ---------------------------------------------
        # RISK
        # ---------------------------------------------

        if strength >= 0.35:

            risk = "HIGH"

        elif strength >= 0.20:

            risk = "MEDIUM"

        else:

            risk = "LOW"

        # ---------------------------------------------
        # RESULT
        # ---------------------------------------------

        results.append({

            "disease":
                disease,

            "peak_month":
                MONTHS[
                    peak_month_num
                ],

            "top_months":
                top_months,

            "seasonality_strength":
                strength,

            "seasonal_risk":
                risk,
        })

    # =================================================
    # SORT
    # =================================================

    results = sorted(

        results,

        key=lambda x:
        x[
            "seasonality_strength"
        ],

        reverse=True,
    )

    print(
        f"✅ Seasonality analysis complete: "
        f"{len(results)} diseases"
    )

    return results