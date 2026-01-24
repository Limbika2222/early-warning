import pandas as pd
from io import BytesIO


def parse_google_trends_csv(file_bytes: bytes) -> pd.DataFrame:
    """
    Definitive Google Trends 'Interest over time' CSV parser.

    Handles:
    - Any Google Trends export
    - Mixed metadata rows
    - Comma or semicolon delimiters
    - Excel-modified CSVs
    """

    text = file_bytes.decode("utf-8", errors="ignore")
    lines = text.splitlines()

    header_index = None
    delimiter = None

    # Step 1: find header row and delimiter
    for i, line in enumerate(lines):
        lower = line.lower()
        if "week" in lower or "date" in lower:
            header_index = i
            if "," in line:
                delimiter = ","
            elif ";" in line:
                delimiter = ";"
            else:
                raise ValueError("Could not determine delimiter")
            break

    if header_index is None:
        raise ValueError("Could not locate Google Trends header row")

    # Step 2: parse CSV starting from header row
    df = pd.read_csv(
        BytesIO(file_bytes),
        skiprows=header_index,
        sep=delimiter,
        engine="python",
    )

    # Step 3: clean columns
    df = df.dropna(axis=1, how="all")

    if df.shape[1] < 2:
        raise ValueError("CSV does not contain interest data")

    df = df.iloc[:, :2]
    df.columns = ["date", "interest_index"]

    # Step 4: safe type conversion
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    df["interest_index"] = pd.to_numeric(
        df["interest_index"], errors="coerce"
    )

    df = df.dropna()

    if df.empty:
        raise ValueError("CSV contains no valid Google Trends rows")

    return df
