import statistics
from collections import defaultdict
import math


class EWMASignalService:
    def __init__(self, alpha=0.3, z_threshold=1.0, min_count=1):
        """
        alpha: smoothing factor
        z_threshold: std deviation threshold for anomaly detection
        min_count: minimum signal strength to consider a spike
        """
        self.alpha = alpha
        self.z_threshold = z_threshold
        self.min_count = min_count

    def compute_ewma(self, values):
        """
        Compute Exponentially Weighted Moving Average
        """
        if not values:
            return []

        ewma = []
        prev = values[0]

        for v in values:
            prev = self.alpha * v + (1 - self.alpha) * prev
            ewma.append(prev)

        return ewma

    def detect_spikes(self, time_series):
        """
        Detect spikes using EWMA-based Z-score (IMPROVED)
        """

        symptom_data = defaultdict(list)

        # 🔹 Organize data per symptom
        for item in time_series:
            symptom = item.get("symptom")
            date = item.get("date")
            count = item.get("count", 0)

            if not symptom or not date:
                continue

            symptom_data[symptom].append((date, count))

        alerts = []

        # 🔹 Process each symptom separately
        for symptom, values in symptom_data.items():
            values.sort(key=lambda x: x[0])

            dates = [v[0] for v in values]
            counts = [v[1] for v in values]

            # 🔥 Require enough history
            if len(counts) < 4:
                continue

            ewma_values = self.compute_ewma(counts)

            # 🔥 Rolling variance (EWMA-based)
            variance = 1

            for i in range(1, len(counts)):
                actual = counts[i]
                expected = ewma_values[i - 1]

                relative_jump = actual / expected if expected > 0 else 0

                variance = max(
                    (1 - self.alpha) * variance + self.alpha * ((actual - expected) ** 2),
                    0.5
                )

                std_dev = math.sqrt(variance)

                z_score = (actual - expected) / std_dev if std_dev > 0 else 0

                if (
                    actual >= self.min_count and
                    (
                        z_score >= self.z_threshold or
                        relative_jump >= 1.5
                    )
                ):
                    alerts.append({
                        "date": dates[i],
                        "symptom": symptom,
                        "actual": actual,
                        "expected": round(expected, 2),
                        "z_score": round(z_score, 2),
                        "type": "SPIKE"
                    })

        return alerts
