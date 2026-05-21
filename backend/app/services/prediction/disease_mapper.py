# =====================================================
# DISEASE MAPPER
# =====================================================

from collections import defaultdict

# =====================================================
# SYMPTOM -> DISEASE RULES
# =====================================================

DISEASE_RULES = {

    "Dengue": [

        "fever",
        "joint pain",
        "rash",
        "skin rash",
        "dengue symptoms",
        "dengue fever",
        "rash dengue",
        "severe headache",
        "muscle aches",
    ],

    "Influenza": [

        "influenza",
        "flu symptoms",
        "flu",
        "cough",
        "sore throat",
        "headache",
        "chills",
        "fatigue",
    ],

    "Malaria": [

        "malaria",
        "fever",
        "night sweats",
        "shivering",
        "sweating",
        "fatigue",
        "headache",
    ],

    "COVID-19": [

        "covid",
        "covid-19",
        "coronavirus",
        "fever",
        "cough",
        "fatigue",
        "headache",
        "sore throat",
        "flu symptoms",
    ],

    "Measles": [

        "measles",
        "fever",
        "skin rash",
        "rash",
        "cough",
    ],

    "Ebola": [

        "ebola",
        "bleeding",
        "vomiting",
        "hemorrhagic fever",
    ],

    "Mpox": [

        "mpox",
        "monkeypox",
        "skin lesions",
        "rash",
    ],
}

# =====================================================
# KEYWORD -> DISEASE
# =====================================================

def map_keyword_to_disease(
    keyword: str
):

    if not keyword:

        return "Unknown"

    keyword = (
        keyword
        .lower()
        .strip()
    )

    for (
        disease,
        keywords,
    ) in DISEASE_RULES.items():

        for item in keywords:

            if item.lower() in keyword:

                return disease

    return "Unknown"

# =====================================================
# COUNTRY NORMALIZER
# =====================================================

def normalize_country(
    value
):

    if not value:
        return "GLOBAL"

    value = str(value).strip()

    mapping = {

        "India": "IN",
        "Malawi": "MW",
        "South Africa": "ZA",
        "United States": "US",
        "Kenya": "KE",
        "Nigeria": "NG",
        "Tanzania": "TZ",
        "Uganda": "UG",
        "Ethiopia": "ET",

        "IN": "IN",
        "MW": "MW",
        "ZA": "ZA",
        "US": "US",
        "KE": "KE",
        "NG": "NG",
        "TZ": "TZ",
        "UG": "UG",
        "ET": "ET",
    }

    return mapping.get(
        value,
        value
    )

# =====================================================
# DISEASE INFERENCE
# =====================================================

def infer_disease_scores(
    predictions
):

    print(
        "🧠 Inferring diseases..."
    )

    disease_scores = defaultdict(

        lambda: {

            "disease": None,

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
    # PROCESS PREDICTIONS
    # =================================================

    for item in predictions:

        disease = item.get(
            "disease",
            "Unknown",
        )

        country = normalize_country(

            item.get(
                "country",
                "GLOBAL",
            )
        )

        # ---------------------------------------------
        # UNIQUE GEO-AWARE KEY
        # ---------------------------------------------

        key = (
            f"{disease}_{country}"
        )

        disease_scores[key][
            "disease"
        ] = disease

        disease_scores[key][
            "country"
        ] = country

        disease_scores[key][
            "google_score"
        ] += item.get(
            "google_score",
            0,
        )

        disease_scores[key][
            "reddit_score"
        ] += item.get(
            "reddit_score",
            0,
        )

        disease_scores[key][
            "who_score"
        ] += item.get(
            "who_score",
            0,
        )

        disease_scores[key][
            "combined_score"
        ] += item.get(
            "combined_score",
            0,
        )

        # ---------------------------------------------
        # KEYWORDS
        # ---------------------------------------------

        for keyword in item.get(
            "matched_keywords",
            [],
        ):

            if (

                keyword
                not in
                disease_scores[key][
                    "matched_keywords"
                ]

            ):

                disease_scores[key][
                    "matched_keywords"
                ].append(
                    keyword
                )

    # =================================================
    # FINALIZE
    # =================================================

    final_results = []

    for _, item in (
        disease_scores.items()
    ):

        score = item[
            "combined_score"
        ]

        # ---------------------------------------------
        # MINIMUM OUTBREAK THRESHOLD
        # ---------------------------------------------

        if score < 500:
            continue

        # ---------------------------------------------
        # RISK LABEL
        # ---------------------------------------------

        if score >= 3000:

            risk = "HIGH"

        elif score >= 1000:

            risk = "MEDIUM"

        else:

            risk = "LOW"

        item[
            "risk_level"
        ] = risk

        # ---------------------------------------------
        # REMOVE DUPLICATES
        # ---------------------------------------------

        item[
            "matched_keywords"
        ] = sorted(

            list(

                set(
                    item[
                        "matched_keywords"
                    ]
                )
            )
        )

        final_results.append(item)

    # =================================================
    # SORT
    # =================================================

    final_results = sorted(

        final_results,

        key=lambda x:
        x["combined_score"],

        reverse=True,
    )

    print(
        f"✅ Diseases inferred: "
        f"{len(final_results)}"
    )

    return final_results