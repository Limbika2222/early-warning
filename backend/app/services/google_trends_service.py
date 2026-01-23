from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError
import pandas as pd
import time
import random


def fetch_google_trends(keyword: str, country_iso2: str, timeframe="today 5-y"):
    """
    Fetch Google Trends interest-over-time data for a single keyword and country.
    Includes rate limiting and graceful failure handling.
    """

    pytrends = TrendReq(
        hl="en-US",
        tz=330,
        timeout=(10, 25),
    )

    try:
        pytrends.build_payload(
            kw_list=[keyword],
            geo=country_iso2,
            timeframe=timeframe,
        )

        df = pytrends.interest_over_time()

        if df.empty:
            return None

        df = df.reset_index()
        df = df.rename(columns={keyword: "interest_index"})
        df["date"] = pd.to_datetime(df["date"]).dt.date

        # polite randomized delay (critical)
        time.sleep(random.uniform(6, 10))

        return df[["date", "interest_index"]]

    except TooManyRequestsError:
        print("    🚫 Google rate limit hit (429). Cooling down...")
        time.sleep(60)
        return None

    except Exception as e:
        print(f"    ⚠ Error: {e}")
        return None
