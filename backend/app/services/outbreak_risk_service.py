# =====================================================
# OUTBREAK SEVERITY MAP
# =====================================================

DISEASE_SEVERITY = {

    # -------------------------------------------------
    # CRITICAL
    # -------------------------------------------------

    "Ebola":
        "CRITICAL",

    "Marburg":
        "CRITICAL",

    # -------------------------------------------------
    # HIGH
    # -------------------------------------------------

    "COVID-19":
        "HIGH",

    "Mpox":
        "HIGH",

    "Cholera":
        "HIGH",

    "Measles":
        "HIGH",

    "Dengue":
        "HIGH",

    "Malaria":
        "HIGH",

    "Influenza":
        "HIGH",

    "Legionnaires Disease":
        "HIGH",

    # -------------------------------------------------
    # MEDIUM
    # -------------------------------------------------

    "Tuberculosis":
        "MEDIUM",

    "Foot and Mouth Disease":
        "MEDIUM",

    # -------------------------------------------------
    # LOW
    # -------------------------------------------------

    "Unknown":
        "LOW",
}

# =====================================================
# GET OUTBREAK SEVERITY
# =====================================================

def get_outbreak_severity(
    disease: str | None
):

    if not disease:

        return "LOW"

    return DISEASE_SEVERITY.get(
        disease,
        "LOW"
    )