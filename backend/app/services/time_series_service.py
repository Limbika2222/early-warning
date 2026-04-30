from collections import defaultdict
from datetime import datetime, timedelta

class TimeSeriesService:

    def generate_time_series(self, signals):
        # 🔥 ONLY USE SIGNAL DATES
        date_symptom_map = {}

        for signal in signals:
            date = signal.get("date")
            if not date:
                continue
            
            symptoms = signal.get("symptoms", [])
            for symptom in symptoms:
                key = (date, symptom)
                date_symptom_map[key] = date_symptom_map.get(key, 0) + 1

        # convert to list
        time_series = [
            {"date": d, "symptom": s, "count": c}
            for (d, s), c in date_symptom_map.items()
        ]

        return time_series

    def fill_missing_dates_per_symptom(self, time_series):

        # group by symptom
        symptom_map = defaultdict(list)

        for item in time_series:
            symptom_map[item["symptom"]].append(item)

        filled = []

        for symptom, records in symptom_map.items():

            # sort by date
            records = sorted(records, key=lambda x: x["date"])

            # ✅ FIX: Skip empty record lists to prevent IndexError
            if not records:
                continue

            start_date = datetime.strptime(records[0]["date"], "%Y-%m-%d")
            end_date = datetime.strptime(records[-1]["date"], "%Y-%m-%d")

            existing_dates = {r["date"]: r["count"] for r in records}

            current = start_date

            while current <= end_date:
                date_str = current.strftime("%Y-%m-%d")

                filled.append({
                    "date": date_str,
                    "symptom": symptom,
                    "count": existing_dates.get(date_str, 0)
                })

                current += timedelta(days=1)

        return filled