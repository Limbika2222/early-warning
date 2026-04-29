import statistics


class EWMASignalService:
    def __init__(self, alpha=0.3, z_threshold=2.0, min_count=2):
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
        Detect spikes using EWMA + Z-score
        """

        symptom_data = {}

        # 🔹 Organize data per symptom
        for item in time_series:
            symptom = item.get("symptom")
            date = item.get("date")
            count = item.get("count", 0)

            if not symptom or not date:
                continue

            symptom_data.setdefault(symptom, []).append((date, count))

        alerts = []

        # 🔹 Process each symptom separately
        for symptom, values in symptom_data.items():
            values.sort(key=lambda x: x[0])

            dates = [v[0] for v in values]
            counts = [v[1] for v in values]

            # 🔥 Require enough history
            if len(counts) < 5:
                continue

            ewma_values = self.compute_ewma(counts)

            # 🔥 Compute statistics
            mean = statistics.mean(counts)
            std_dev = statistics.pstdev(counts)

            if std_dev == 0:
                continue

            for i in range(1, len(counts)):
                actual = counts[i]
                expected = ewma_values[i - 1]

                # 🔥 Z-score calculation
                z_score = (actual - mean) / std_dev

                # 🔥 FINAL SPIKE CONDITION (production-grade)
                if (
                    actual >= self.min_count and        # ignore weak signals
                    z_score >= self.z_threshold and     # statistically significant
                    actual > expected                  # above EWMA baseline
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