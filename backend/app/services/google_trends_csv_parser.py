import pandas as pd
import io
import re


def parse_google_trends_csv(file_bytes: bytes) -> pd.DataFrame:
    """
    Production-safe Google Trends CSV parser.

    Handles:
    - Metadata rows at top
    - "Interest over time" header noise
    - Comma or semicolon delimiters
    - Excel-modified files
    - Empty lines
    - Different Google export formats
    """

    try:
        # ---------------------------------------
        # Decode safely
        # ---------------------------------------
        text = file_bytes.decode("utf-8-sig", errors="ignore")
        lines = text.splitlines()

        if not lines:
            raise ValueError("Empty CSV file")

        # ---------------------------------------
        # Detect header row dynamically
        # ---------------------------------------
        header_index = None
        delimiter = ","

        for i, line in enumerate(lines):
            lower = line.lower()

            if "date" in lower or "week" in lower:
                header_index = i

                # detect delimiter
                if ";" in line:
                    delimiter = ";"
                elif "," in line:
                    delimiter = ","
                else:
                    raise ValueError("Could not determine CSV delimiter")

                break

        if header_index is None:
            raise ValueError("Could not locate Google Trends header row")

        # ---------------------------------------
        # Reconstruct clean CSV from header row
        # ---------------------------------------
        cleaned_csv = "\n".join(lines[header_index:])

        df = pd.read_csv(
            io.StringIO(cleaned_csv),
            sep=delimiter,
            engine="python",
        )

        # ---------------------------------------
        # Clean dataframe
        # ---------------------------------------
        df = df.dropna(axis=1, how="all")

        if df.shape[1] < 2:
            raise ValueError("CSV does not contain interest data")

        # Keep first two columns only
        df = df.iloc[:, :2]
        df.columns = ["date", "interest_index"]

        # ---------------------------------------
        # Convert safely
        # ---------------------------------------
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
        df["interest_index"] = pd.to_numeric(
            df["interest_index"], errors="coerce"
        )

        df = df.dropna()

        if df.empty:
            raise ValueError("CSV contains no valid Google Trends rows")

        return df

    except Exception as e:
        raise ValueError("Invalid Google Trends CSV format")