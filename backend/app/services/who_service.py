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
# FETCH OUTBREAK REPORTS
# =====================================================

def fetch_who_outbreak_news():

    print(
        "🌍 Fetching GDELT outbreak reports..."
    )

    try:

        params = {

            "query":
                "disease outbreak",

            "mode":
                "artlist",

            "maxrecords":
                10,

            "format":
                "json",
        }

        response = requests.get(

            GDELT_URL,

            params=params,

            headers={
                "User-Agent":
                    "Mozilla/5.0"
            },

            timeout=30,
        )

        print(
            "🔥 STATUS:",
            response.status_code
        )

        # -------------------------------------------------
        # RATE LIMIT
        # -------------------------------------------------

        if response.status_code == 429:

            print(
                "⚠️ GDELT rate limited"
            )

            return []

        response.raise_for_status()

        # -------------------------------------------------
        # SAFE JSON
        # -------------------------------------------------

        try:

            data = response.json()

        except Exception:

            print(
                "❌ Invalid JSON"
            )

            print(
                response.text[:500]
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

            reports.append({

                "title":
                    title,

                "published":
                    article.get(
                        "seendate",
                        ""
                    ),

                "country":
                    extract_country(
                        title
                    ),

                "source":
                    article.get(
                        "domain",
                        ""
                    ),

                "url":
                    article.get(
                        "url",
                        ""
                    ),

                "disease":
                    extract_disease(
                        title
                    ),
            })

        print(
            f"✅ Reports fetched: "
            f"{len(reports)}"
        )

        return reports

    except Exception as e:

        print(
            "❌ GDELT error:",
            str(e)
        )

        return []