import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.google_trends_csv_parser import parse_google_trends_csv
from app.services.google_trends_store import store_parsed_csv_data

DATA_FOLDER = "data/google_trends"

total_rows = 0

for filename in os.listdir(DATA_FOLDER):
    if filename.endswith(".csv"):
        file_path = os.path.join(DATA_FOLDER, filename)

        print("Processing:", filename)

        with open(file_path, "rb") as f:
            file_bytes = f.read()

        data = parse_google_trends_csv(file_bytes)
        rows = store_parsed_csv_data(data)

        print("Inserted rows:", rows)
        total_rows += rows

print("Total rows inserted:", total_rows)