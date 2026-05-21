import time
import requests

from app.services.who_parser import (
    extract_disease,
    extract_country,
)

# =====================================================
# GDELT API
# =====================================================

GDELT_URL = (
    "https://api.gdeltproject.org/api/v2/"
    "doc/doc"
)

# =====================================================
# QUERY
# =====================================================

OUTBREAK_QUERY = (
    '("disease outbreak" OR '
    'cholera OR dengue OR malaria OR '
    'influenza OR measles OR mpox OR '
    'ebola OR marburg OR tuberculosis OR '
    '"legionnaires disease")'
)

# =====================================================
# REQUEST HEADERS
# =====================================================

HEADERS = {

    "User-Agent":
        (
            "Mozilla/5.0 "
            "(X11; Linux x86_64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/122.0 Safari/537.36"
        ),

    "Accept":
        "application/json",
}

# =====================================================
# SAFE JSON PARSER
# =====================================================

def safe_json_response(
    response
):

    try:

        return response.json()

    except Exception:

        print(
            "❌ Invalid JSON response"
        )

        preview = (
            response.text[:500]
        )

        print(
            "🔥 RESPONSE PREVIEW:"
        )

        print(preview)

        return None

# =====================================================
# FETCH GDELT OUTBREAK REPORTS
# =====================================================

def fetch_who_outbreak_news():

    print(
        "🌍 Fetching outbreak intelligence..."
    )

    # =================================================
    # PARAMETERS
    # =================================================

    params = {

        "query":
            OUTBREAK_QUERY,

        "mode":
            "artlist",

        "maxrecords":
            10,

        "format":
            "json",

        "sort":
            "datedesc",
    }

    # =================================================
    # RETRY LOOP
    # =================================================

    max_attempts = 3

    for attempt in range(
        max_attempts
    ):

        try:

            print(
                f"🔄 Attempt "
                f"{attempt + 1}/"
                f"{max_attempts}"
            )

            # -----------------------------------------
            # RATE LIMIT PROTECTION
            # -----------------------------------------

            time.sleep(2)

            response = requests.get(

                GDELT_URL,

                params=params,

                headers=HEADERS,

                timeout=30,
            )

            print(
                "🔥 STATUS:",
                response.status_code
            )

            # -----------------------------------------
            # SUCCESS
            # -----------------------------------------

            if (
                response.status_code
                == 200
            ):

                data = safe_json_response(
                    response
                )

                if not data:

                    return []

                # -------------------------------------
                # GDELT ERROR RESPONSE
                # -------------------------------------

                if isinstance(
                    data,
                    dict
                ) and data.get(
                    "errors"
                ):

                    print(
                        "❌ GDELT returned errors:"
                    )

                    print(
                        data.get(
                            "errors"
                        )
                    )

                    return []

                articles = data.get(
                    "articles",
                    []
                )

                print(
                    f"📊 ARTICLES FOUND: "
                    f"{len(articles)}"
                )

                reports = []

                for article in articles:

                    title = article.get(
                        "title",
                        ""
                    )

                    if not title:

                        continue

                    # ---------------------------------
                    # COUNTRY EXTRACTION
                    # ---------------------------------

                    country = (
                        extract_country(
                            title
                        )
                    )

                    # fallback to sourcecountry
                    if (
                        country["iso2"]
                        is None
                    ):

                        source_country = (
                            article.get(
                                "sourcecountry",
                                ""
                            )
                        )

                        if source_country:

                            country = (
                                extract_country(
                                    source_country
                                )
                            )

                    # ---------------------------------
                    # DISEASE EXTRACTION
                    # ---------------------------------

                    disease = (
                        extract_disease(
                            title
                        )
                    )

                    report = {

                        "title":
                            title,

                        "published":
                            article.get(
                                "seendate",
                                ""
                            ),

                        "country":
                            country,

                        "source":
                            article.get(
                                "domain",
                                "Unknown"
                            ),

                        "url":
                            article.get(
                                "url",
                                ""
                            ),

                        "disease":
                            disease,
                    }

                    reports.append(
                        report
                    )

                print(
                    f"✅ Reports fetched: "
                    f"{len(reports)}"
                )

                return reports

            # -----------------------------------------
            # RATE LIMITED
            # -----------------------------------------

            elif (
                response.status_code
                == 429
            ):

                wait_time = (
                    5 * (attempt + 1)
                )

                print(
                    "⚠️ GDELT rate limited"
                )

                print(
                    f"⏳ Waiting "
                    f"{wait_time}s..."
                )

                time.sleep(wait_time)

            # -----------------------------------------
            # SERVER ERROR
            # -----------------------------------------

            elif (
                response.status_code
                >= 500
            ):

                print(
                    "⚠️ GDELT server error"
                )

                time.sleep(5)

            # -----------------------------------------
            # OTHER ERRORS
            # -----------------------------------------

            else:

                print(
                    "❌ Unexpected status:"
                )

                print(
                    response.status_code
                )

                preview = (
                    response.text[:500]
                )

                print(preview)

                return []

        except requests.Timeout:

            print(
                "⏰ Request timeout"
            )

        except requests.RequestException as e:

            print(
                "❌ Network error:"
            )

            print(str(e))

        except Exception as e:

            print(
                "❌ Unknown error:"
            )

            print(str(e))

    # =================================================
    # FAILED AFTER RETRIES
    # =================================================

    print(
        "❌ Failed after retries"
    )

    return []