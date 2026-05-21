# =====================================================
# DISEASE MAPPER
# =====================================================
# Converts:
#
# symptoms / keywords
#
# INTO:
#
# probable diseases
# =====================================================

from collections import defaultdict

# =====================================================
# SYMPTOM -> DISEASE RULES
# =====================================================

DISEASE_RULES = {

    # -------------------------------------------------
    # DENGUE
    # -------------------------------------------------

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

    # -------------------------------------------------
    # INFLUENZA
    # -------------------------------------------------

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

    # -------------------------------------------------
    # MALARIA
    # -------------------------------------------------

    "Malaria": [

        "malaria",

        "fever",

        "night sweats",

        "shivering",

        "sweating",

        "fatigue",

        "headache",
    ],

    # -------------------------------------------------
    # COVID-19
    # -------------------------------------------------

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

    # -------------------------------------------------
    # MEASLES
    # -------------------------------------------------

    "Measles": [

        "measles",

        "fever",

        "skin rash",

        "rash",

        "cough",
    ],

    # -------------------------------------------------
    # EBOLA
    # -------------------------------------------------

    "Ebola": [

        "ebola",

        "bleeding",

        "vomiting",

        "hemorrhagic fever",
    ],

    # -------------------------------------------------
    # MPOX
    # -------------------------------------------------

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

    # -------------------------------------------------
    # MATCH
    # -------------------------------------------------

    for (
        disease,
        keywords,
    ) in DISEASE_RULES.items():

        for item in keywords:

            if item.lower() in keyword:

                return disease

    return "Unknown"

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

        keyword = (

            item.get(
                "disease",
                "",
            )

            .lower()

            .strip()
        )

        for (
            disease,
            symptom_list,
        ) in DISEASE_RULES.items():

            matches = [

                s.lower()
                for s in symptom_list
            ]

            if keyword in matches:

                disease_scores[disease][
                    "disease"
                ] = disease

                disease_scores[disease][
                    "country"
                ] = item.get(
                    "country",
                    "GLOBAL",
                )

                disease_scores[disease][
                    "google_score"
                ] += item.get(
                    "google_score",
                    0,
                )

                disease_scores[disease][
                    "reddit_score"
                ] += item.get(
                    "reddit_score",
                    0,
                )

                disease_scores[disease][
                    "who_score"
                ] += item.get(
                    "who_score",
                    0,
                )

                disease_scores[disease][
                    "combined_score"
                ] += item.get(
                    "combined_score",
                    0,
                )

                disease_scores[disease][
                    "matched_keywords"
                ].append(keyword)

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

        # -------------------------------------------------
        # RISK LABEL
        # -------------------------------------------------

        if score >= 1000:

            risk = "HIGH"

        elif score >= 200:

            risk = "MEDIUM"

        else:

            risk = "LOW"

        item[
            "risk_level"
        ] = risk

        # -------------------------------------------------
        # REMOVE DUPLICATES
        # -------------------------------------------------

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