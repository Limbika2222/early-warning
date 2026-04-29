from collections import defaultdict
from datetime import datetime, timedelta


class TimeSeriesService:

    def generate_time_series(self, signals):
        time_series = defaultdict(lambda: defaultdict(int))

        for signal in signals:
            date = signal.get("date")
            symptoms = signal.get("symptoms", [])

            for symptom in symptoms:
                time_series[date][symptom] += 1

        return dict(time_series)

    def fill_missing_dates_per_symptom(self, time_series):
        """
        Fill missing dates for EACH symptom separately
        """

        all_dates = sorted(time_series.keys())
        if not all_dates:
            return []

        start = datetime.strptime(all_dates[0], "%Y-%m-%d")
        end = datetime.strptime(all_dates[-1], "%Y-%m-%d")

        # 🔹 collect all symptoms
        all_symptoms = set()
        for symptoms in time_series.values():
            all_symptoms.update(symptoms.keys())

        result = []

        for symptom in all_symptoms:
            current = start

            while current <= end:
                date_str = current.strftime("%Y-%m-%d")

                count = time_series.get(date_str, {}).get(symptom, 0)

                result.append({
                    "date": date_str,
                    "symptom": symptom,
                    "count": count
                })

                current += timedelta(days=1)

        return result