import pandas as pd
import io
import re


# -------------------------------------------------
# 🔥 Clean keyword (SAFE)
# -------------------------------------------------
def clean_keyword(keyword: str) -> str:
    if not keyword:
        return ""

    keyword = str(keyword).strip()

    # remove ": something"
    keyword = re.sub(r":.*", "", keyword)

    # remove "(something)"
    keyword = re.sub(r"\(.*?\)", "", keyword)

    # remove % and normalize spaces
    keyword = keyword.replace("%", "")
    keyword = re.sub(r"\s+", " ", keyword)

    return keyword.lower().strip()


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
# 🔥 FINAL UNIVERSAL PARSER
# -------------------------------------------------
def parse_google_trends_csv(file_bytes: bytes):
    print("🔥 PARSER RUNNING (UNIVERSAL VERSION)")

    try:
        text = file_bytes.decode("utf-8-sig", errors="ignore")
        lines = [line for line in text.splitlines() if line.strip()]

        if not lines:
            raise ValueError("Empty CSV file")

        # -------------------------------------------------
        # 🔥 STEP 1: Find header row (VERY ROBUST)
        # -------------------------------------------------
        header_index = None
        delimiter = ","

        for i, line in enumerate(lines):
            # detect delimiter
            if ";" in line:
                delimiter = ";"
            else:
                delimiter = ","

            cols = [c.strip() for c in line.split(delimiter)]

            # must have at least 2+ columns
            if len(cols) < 2:
                continue

            # first column should be date-like OR text
            first = cols[0].lower()

            # second column must NOT be numeric (prevents picking data row)
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

        # drop empty columns
        df = df.dropna(axis=1, how="all")

        if df.shape[1] < 2:
            raise ValueError("No keyword columns found")

        # -------------------------------------------------
        # STEP 3: Rename first column → date
        # -------------------------------------------------
        df.rename(columns={df.columns[0]: "date"}, inplace=True)

        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
        df = df.dropna(subset=["date"])

        # -------------------------------------------------
        # STEP 4: Clean column names safely
        # -------------------------------------------------
        column_map = {}
        valid_columns = []

        for col in df.columns[1:]:
            cleaned = clean_keyword(col)

            # skip invalid columns
            if not cleaned or cleaned.replace(".", "").isdigit():
                print(f"[WARNING] Skipping column: {col}")
                continue

            column_map[col] = cleaned
            valid_columns.append(col)

        print("[DEBUG] Column map:", column_map)

        if not valid_columns:
            raise ValueError("No valid keyword columns")

        # -------------------------------------------------
        # STEP 5: Convert to LONG format
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

        # -------------------------------------------------
        # DEBUG OUTPUT
        # -------------------------------------------------
        print(f"[PARSER] Rows extracted: {len(data)}")
        print(f"[PARSER SAMPLE]: {data[:5]}")

        return data

    except Exception as e:
        print("[PARSER ERROR]", str(e))
        raise ValueError(f"Invalid Google Trends CSV format: {str(e)}")