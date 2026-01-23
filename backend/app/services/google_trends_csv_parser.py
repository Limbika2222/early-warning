import pandas as pd
from io import BytesIO


def parse_google_trends_csv(file_bytes: bytes) -> pd.DataFrame:
    """
    Parse Google Trends 'Interest over time' CSV.

    Returns a DataFrame with:
    - date (datetime.date)
    - interest_index (int)
    """

    # Read CSV, skip metadata row
    df = pd.read_csv(BytesIO(file_bytes), skiprows=1)

    if df.shape[1] != 2:
        raise ValueError("Unexpected Google Trends CSV format")

    df.columns = ["date", "interest_index"]

    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["interest_index"] = df["interest_index"].astype(int)

    return df
