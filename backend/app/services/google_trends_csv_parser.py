import pandas as pd
import io
import re


# -------------------------------------------------
# 🔥 Clean keyword (FIXED)
# -------------------------------------------------
def clean_keyword(keyword: str) -> str:
    if not keyword:
        return ""

    keyword = str(keyword).strip()

    # -------------------------------------------------
    # 🔥 REMOVE GOOGLE DUPLICATES (.1, .2, etc)
    # -------------------------------------------------
    keyword = re.sub(r"\.\d+$", "", keyword)

    # -------------------------------------------------
    # REMOVE EXTRA TEXT
    # -------------------------------------------------
    keyword = re.sub(r":.*", "", keyword)          # remove ": something"
    keyword = re.sub(r"\(.*?\)", "", keyword)      # remove "(...)"

    # -------------------------------------------------
    # NORMALIZATION (CRITICAL)
    # -------------------------------------------------
    keyword = keyword.lower()

    keyword = keyword.replace("symptoms of", "")
    keyword = keyword.replace("symptom of", "")
    keyword = keyword.replace("covid-19", "covid")
    keyword = keyword.replace("influenza-like illness", "flu")

    # clean separators
    keyword = keyword.replace("-", " ")
    keyword = keyword.replace("_", " ")

    # remove % and normalize spaces
    keyword = keyword.replace("%", "")
    keyword = re.sub(r"\s+", " ", keyword)

    return keyword.strip()


# -------------------------------------------------
# 🔥 SAFE VALUE PARSER
# -------------------------------------------------
def parse_value(value):
    if pd.isna(value):
        return 0

    value = str(value).strip()

    if value == "<1":
        return 0

    try:
        return int(float(value))
    except:
        return 0


# -------------------------------------------------
# 🔥 FINAL UNIVERSAL PARSER (DEDUP FIXED)
# -------------------------------------------------
def parse_google_trends_csv(file_bytes: bytes):
    print("🔥 PARSER RUNNING (FIXED VERSION)")

    try:
        text = file_bytes.decode("utf-8-sig", errors="ignore")
        lines = [line for line in text.splitlines() if line.strip()]

        if not lines:
            raise ValueError("Empty CSV file")

        # -------------------------------------------------
        # STEP 1: Detect header
        # -------------------------------------------------
        header_index = None
        delimiter = ","

        for i, line in enumerate(lines):
            delimiter = ";" if ";" in line else ","
            cols = [c.strip() for c in line.split(delimiter)]

            if len(cols) < 2:
                continue

            second = cols[1]

            if not second.replace(".", "").isdigit():
                header_index = i
                break

        if header_index is None:
            raise ValueError("Could not detect header row")

        print(f"[DEBUG] Header detected at line: {header_index}")

        # -------------------------------------------------
        # STEP 2: Build dataframe
        # -------------------------------------------------
        cleaned_csv = "\n".join(lines[header_index:])

        df = pd.read_csv(
            io.StringIO(cleaned_csv),
            sep=delimiter,
            engine="python"
        )

        df = df.dropna(axis=1, how="all")

        if df.shape[1] < 2:
            raise ValueError("No keyword columns found")

        # -------------------------------------------------
        # STEP 3: DATE
        # -------------------------------------------------
        df.rename(columns={df.columns[0]: "date"}, inplace=True)

        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
        df = df.dropna(subset=["date"])

        # -------------------------------------------------
        # STEP 4: CLEAN + DEDUP COLUMNS
        # -------------------------------------------------
        column_map = {}
        valid_columns = []
        seen_keywords = set()

        for col in df.columns[1:]:
            cleaned = clean_keyword(col)

            if not cleaned or cleaned.replace(".", "").isdigit():
                print(f"[WARNING] Skipping column: {col}")
                continue

            # 🔥 DEDUPLICATION (KEY FIX)
            if cleaned in seen_keywords:
                print(f"[INFO] Duplicate removed: {col} → {cleaned}")
                continue

            seen_keywords.add(cleaned)

            column_map[col] = cleaned
            valid_columns.append(col)

        print("[DEBUG] Column map:", column_map)

        if not valid_columns:
            raise ValueError("No valid keyword columns")

        # -------------------------------------------------
        # STEP 5: LONG FORMAT
        # -------------------------------------------------
        data = []

        for _, row in df.iterrows():
            date_val = row["date"]

            for col in valid_columns:
                keyword = column_map[col]
                interest = parse_value(row[col])

                data.append({
                    "keyword": keyword,
                    "date": date_val,
                    "interest": interest,
                })

        if not data:
            raise ValueError("No valid rows extracted")

        print(f"[PARSER] Rows extracted: {len(data)}")
        print(f"[PARSER SAMPLE]: {data[:5]}")

        return data

    except Exception as e:
        print("[PARSER ERROR]", str(e))
        raise ValueError(f"Invalid Google Trends CSV format: {str(e)}")