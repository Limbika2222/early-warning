# =====================================================
# WHO / GDELT PARSER
# =====================================================

import re

# =====================================================
# DISEASE ALIASES
# =====================================================

DISEASE_ALIASES = {

    # Viral
    "ebola": "Ebola",
    "marburg": "Marburg",
    "mpox": "Mpox",
    "monkeypox": "Mpox",
    "covid": "COVID-19",
    "covid-19": "COVID-19",
    "coronavirus": "COVID-19",
    "sars-cov-2": "COVID-19",

    # Mosquito-borne
    "dengue": "Dengue",
    "dengue fever": "Dengue",
    "malaria": "Malaria",
    "zika": "Zika",
    "yellow fever": "Yellow Fever",
    "chikungunya": "Chikungunya",

    # Respiratory
    "influenza": "Influenza",
    "avian influenza": "Influenza",
    "bird flu": "Influenza",
    "flu": "Influenza",
    "h5n1": "Influenza",
    "rsv": "RSV",

    # Bacterial
    "cholera": "Cholera",
    "tuberculosis": "Tuberculosis",
    "tb": "Tuberculosis",
    "tuberkulose": "Tuberculosis",
    "legionnaires disease": "Legionnaires Disease",
    "plague": "Plague",
    "anthrax": "Anthrax",

    # Childhood
    "measles": "Measles",
    "polio": "Polio",

    # Other
    "rabies": "Rabies",
    "meningitis": "Meningitis",
    "lassa fever": "Lassa Fever",
    "nipah": "Nipah Virus",
    "norovirus": "Norovirus",
    "hantavirus": "Hantavirus",
    "hepatitis": "Hepatitis",
    "pneumonia": "Pneumonia",
}

# =====================================================
# COUNTRY MAP
# =====================================================

COUNTRY_MAP = {

    # Africa
    "uganda": "UG",
    "kenya": "KE",
    "tanzania": "TZ",
    "ethiopia": "ET",
    "nigeria": "NG",
    "cameroon": "CM",
    "ghana": "GH",
    "zambia": "ZM",
    "mozambique": "MZ",
    "malawi": "MW",
    "rwanda": "RW",
    "sudan": "SD",
    "south sudan": "SS",

    # Congo variants
    "democratic republic of the congo": "CD",
    "democratic republic of congo": "CD",
    "dr congo": "CD",
    "drc": "CD",
    "kinshasa": "CD",
    "congo": "CG",

    # Europe
    "germany": "DE",
    "france": "FR",
    "greece": "GR",

    # UK variants
    "united kingdom": "GB",
    "england": "GB",
    "scotland": "GB",
    "wales": "GB",
    "london": "GB",
    "uk": "GB",

    # America
    "united states": "US",
    "usa": "US",
    "america": "US",
    "canada": "CA",

    # Asia
    "india": "IN",
    "china": "CN",
    "russia": "RU",
    "krievijā": "RU",
}

# =====================================================
# ISO2 -> DISPLAY NAME
# =====================================================

ISO2_TO_NAME = {

    "UG": "Uganda",
    "KE": "Kenya",
    "TZ": "Tanzania",
    "ET": "Ethiopia",
    "NG": "Nigeria",
    "CM": "Cameroon",
    "GH": "Ghana",
    "ZM": "Zambia",
    "MZ": "Mozambique",
    "MW": "Malawi",
    "RW": "Rwanda",
    "SD": "Sudan",
    "SS": "South Sudan",

    "CD": "DR Congo",
    "CG": "Congo",

    "GB": "United Kingdom",
    "US": "United States",
    "CA": "Canada",

    "DE": "Germany",
    "FR": "France",
    "GR": "Greece",

    "IN": "India",
    "CN": "China",
    "RU": "Russia",
}

# =====================================================
# HOTSPOT PRIORITY
# =====================================================

DISEASE_PRIORITY_COUNTRIES = {

    "Ebola": [
        "CD",
        "UG",
        "SD",
        "RW",
    ],

    "Marburg": [
        "TZ",
        "UG",
        "GH",
        "RW",
    ],

    "Mpox": [
        "CD",
        "NG",
        "CM",
    ],

    "Cholera": [
        "MW",
        "ZM",
        "MZ",
        "ET",
        "SD",
    ],
}

# =====================================================
# IGNORE COUNTRIES
# Helps prevent reporting-country errors
# =====================================================

IGNORE_FOR_DISEASE = {

    "Ebola": [
        "GB",
        "US",
        "CA",
    ],

    "Marburg": [
        "GB",
        "US",
    ],
}

# =====================================================
# NORMALIZE
# =====================================================

def normalize_text(text: str):

    text = text.lower()

    text = re.sub(
        r"[^\w\s\-]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()

# =====================================================
# EXTRACT DISEASE
# =====================================================

def extract_disease(title: str):

    title_lower = (
        title
        .lower()
        .strip()
    )

    # -------------------------------------------------
    # PRIORITY ORDER
    # LONGEST MATCH FIRST
    # -------------------------------------------------

    aliases = sorted(
        DISEASE_ALIASES.keys(),
        key=len,
        reverse=True,
    )

    for alias in aliases:

        pattern = (
            r"\b"
            + re.escape(alias.lower())
            + r"\b"
        )

        if re.search(
            pattern,
            title_lower,
        ):

            return DISEASE_ALIASES[
                alias
            ]

    return "Unknown"

# =====================================================
# COUNTRY EXTRACTION
# =====================================================

def extract_country(title: str):

    title = normalize_text(title)

    disease = extract_disease(title)

    # =================================================
    # EBOLA / MARBURG SPECIAL RULES
    # =================================================

    if disease in ["Ebola", "Marburg"]:

        hotspot_terms = {

            "uganda": "UG",

            "congo": "CD",

            "drc": "CD",

            "dr congo": "CD",

            "democratic republic of the congo": "CD",

            "rwanda": "RW",

            "sudan": "SD",

            "tanzania": "TZ",
        }

        # -------------------------------------------------
        # ONLY TRUST HOTSPOTS
        # -------------------------------------------------

        for country, iso2 in hotspot_terms.items():

            pattern = (
                r"\b"
                + re.escape(country)
                + r"\b"
            )

            if re.search(pattern, title):

                return {

                    "name":
                        country.title(),

                    "iso2":
                        iso2,
                }

        # -------------------------------------------------
        # OTHERWISE UNKNOWN
        # -------------------------------------------------

        return {

            "name":
                "Unknown",

            "iso2":
                None,
        }

    # =================================================
    # NORMAL COUNTRY LOGIC
    # =================================================

    sorted_terms = sorted(
        COUNTRY_MAP.keys(),
        key=len,
        reverse=True,
    )

    for country in sorted_terms:

        pattern = (
            r"\b"
            + re.escape(country)
            + r"\b"
        )

        if re.search(pattern, title):

            return {

                "name":
                    country.title(),

                "iso2":
                    COUNTRY_MAP[country],
            }

    return {

        "name":
            "Unknown",

        "iso2":
            None,
    }
