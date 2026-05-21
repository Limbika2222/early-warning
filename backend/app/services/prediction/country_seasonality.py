# =====================================================
# COUNTRY-SPECIFIC SEASONALITY RULES
# =====================================================

COUNTRY_SEASONALITY = {

    # =================================================
    # SOUTH AFRICA
    # =================================================

    "ZA": {

        "Influenza": {
            "peak_month": "June",
            "top_months": [
                "June",
                "July",
                "August",
            ],
            "seasonality_strength": 0.92,
        },

        "Malaria": {
            "peak_month": "January",
            "top_months": [
                "December",
                "January",
                "February",
            ],
            "seasonality_strength": 0.85,
        },

        "Dengue": {
            "peak_month": "March",
            "top_months": [
                "February",
                "March",
                "April",
            ],
            "seasonality_strength": 0.72,
        },
    },

    # =================================================
    # INDIA
    # =================================================

    "IN": {

        "Influenza": {
            "peak_month": "December",
            "top_months": [
                "November",
                "December",
                "January",
            ],
            "seasonality_strength": 0.80,
        },

        "Dengue": {
            "peak_month": "September",
            "top_months": [
                "August",
                "September",
                "October",
            ],
            "seasonality_strength": 0.95,
        },

        "Malaria": {
            "peak_month": "July",
            "top_months": [
                "June",
                "July",
                "August",
            ],
            "seasonality_strength": 0.88,
        },
    },

    # =================================================
    # MALAWI
    # =================================================

    "MW": {

        "Malaria": {
            "peak_month": "January",
            "top_months": [
                "December",
                "January",
                "February",
            ],
            "seasonality_strength": 0.94,
        },

        "Influenza": {
            "peak_month": "July",
            "top_months": [
                "June",
                "July",
                "August",
            ],
            "seasonality_strength": 0.71,
        },
    },

    # =================================================
    # UGANDA
    # =================================================

    "UG": {

        "Ebola": {
            "peak_month": "September",
            "top_months": [
                "September",
                "October",
            ],
            "seasonality_strength": 0.60,
        },

        "Malaria": {
            "peak_month": "May",
            "top_months": [
                "April",
                "May",
                "June",
            ],
            "seasonality_strength": 0.90,
        },
    },
}