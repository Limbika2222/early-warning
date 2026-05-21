from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.google_trends import (
    GoogleTrendsTimeseries,
)

from app.models.who_outbreaks import (
    WhoOutbreakReport,
)

from app.services.prediction.disease_mapper import (
    map_keyword_to_disease,
)

# =====================================================
# OPTIONAL REDDIT MODEL
# =====================================================

try:

    from app.models.reddit_signal import (
        RedditSignal,
    )

except Exception:

    RedditSignal = None


# =====================================================
# SAFE ATTRIBUTE ACCESS
# =====================================================

def safe_getattr(
    obj,
    attr,
    default=None,
):

    try:

        return getattr(obj, attr)

    except Exception:

        return default


# =====================================================
# RISK LABEL
# =====================================================

def calculate_risk_level(
    score: float
):

    if score >= 3000:
        return "HIGH"

    if score >= 1000:
        return "MEDIUM"

    return "LOW"


# =====================================================
# FEATURE BUILDER
# =====================================================

def build_prediction_features(
    db: Session
):

    print(
        "🧠 Building prediction features..."
    )

    # =================================================
    # STORAGE
    # =================================================

    features = defaultdict(
        lambda: {

            "disease": "Unknown",

            "country": "GLOBAL",

            "google_score": 0,

            "reddit_score": 0,

            "who_score": 0,

            "combined_score": 0,

            "matched_keywords": [],

            "risk_level": "LOW",
        }
    )

    # =================================================
    # GOOGLE TRENDS DATA
    # =================================================

    try:

        google_rows = (

            db.query(
                GoogleTrendsTimeseries
            ).all()
        )

        print(
            f"📈 Google rows: "
            f"{len(google_rows)}"
        )

        for row in google_rows:

            # -----------------------------------------
            # KEYWORD
            # -----------------------------------------

            keyword_obj = safe_getattr(
                row,
                "keyword",
            )

            keyword_text = None

            if keyword_obj:

                keyword_text = safe_getattr(
                    keyword_obj,
                    "keyword_text",
                )

            if not keyword_text:
                continue

            # -----------------------------------------
            # MAP TO DISEASE
            # -----------------------------------------

            disease = map_keyword_to_disease(
                keyword_text
            )

            key = disease.lower()

            features[key][
                "disease"
            ] = disease

            # -----------------------------------------
            # COUNTRY
            # -----------------------------------------

            country_obj = safe_getattr(
                row,
                "country",
            )

            if country_obj:

                iso2 = safe_getattr(
                    country_obj,
                    "iso2",
                )

                if iso2:

                    features[key][
                        "country"
                    ] = iso2

            # -----------------------------------------
            # INTEREST SCORE
            # -----------------------------------------

            interest = safe_getattr(
                row,
                "interest_index",
                0,
            )

            features[key][
                "google_score"
            ] += float(
                interest or 0
            )

            # -----------------------------------------
            # MATCHED KEYWORDS
            # -----------------------------------------

            if (

                keyword_text
                not in
                features[key][
                    "matched_keywords"
                ]

            ):

                features[key][
                    "matched_keywords"
                ].append(
                    keyword_text
                )

    except Exception as e:

        print(
            "⚠️ Google feature error:",
            str(e)
        )

    # =================================================
    # REDDIT SIGNALS
    # =================================================

    if RedditSignal:

        try:

            reddit_rows = (

                db.query(
                    RedditSignal
                ).all()
            )

            print(
                f"💬 Reddit rows: "
                f"{len(reddit_rows)}"
            )

            for row in reddit_rows:

                disease = safe_getattr(
                    row,
                    "disease",
                    "Unknown",
                )

                if not disease:
                    continue

                key = disease.lower()

                features[key][
                    "disease"
                ] = disease

                # -------------------------------------
                # SIGNAL STRENGTH
                # -------------------------------------

                signal_strength = safe_getattr(
                    row,
                    "signal_strength",
                    0,
                )

                features[key][
                    "reddit_score"
                ] += float(
                    signal_strength or 0
                )

        except Exception as e:

            print(
                "⚠️ Reddit feature error:",
                str(e)
            )

    # =================================================
    # WHO OUTBREAK SIGNALS
    # =================================================

    try:

        who_rows = (

            db.query(
                WhoOutbreakReport
            ).all()
        )

        print(
            f"🌍 WHO rows: "
            f"{len(who_rows)}"
        )

        for row in who_rows:

            disease = safe_getattr(
                row,
                "disease",
                "Unknown",
            )

            if (
                not disease
                or disease == "Unknown"
            ):
                continue

            key = disease.lower()

            features[key][
                "disease"
            ] = disease

            # -----------------------------------------
            # COUNTRY
            # -----------------------------------------

            iso2 = safe_getattr(
                row,
                "country_iso2",
            )

            if iso2:

                features[key][
                    "country"
                ] = iso2

            # -----------------------------------------
            # WHO SEVERITY
            # -----------------------------------------

            severity = safe_getattr(
                row,
                "severity",
                "LOW",
            )

            if severity == "HIGH":

                features[key][
                    "who_score"
                ] += 40

            elif severity == "MEDIUM":

                features[key][
                    "who_score"
                ] += 25

            else:

                features[key][
                    "who_score"
                ] += 10

    except Exception as e:

        print(
            "⚠️ WHO feature error:",
            str(e)
        )

    # =================================================
    # FINALIZE
    # =================================================

    results = []

    for _, item in (
        features.items()
    ):

        combined = (

            item["google_score"]

            + item["reddit_score"]

            + item["who_score"]
        )

        item[
            "combined_score"
        ] = round(
            combined,
            2,
        )

        item[
            "risk_level"
        ] = calculate_risk_level(
            combined
        )

        results.append(item)

    # =================================================
    # SORT
    # =================================================

    results = sorted(

        results,

        key=lambda x:
        x["combined_score"],

        reverse=True,
    )

    print(
        f"✅ Prediction features built: "
        f"{len(results)}"
    )

    return results