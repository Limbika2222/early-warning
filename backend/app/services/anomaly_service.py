from app.utils.statistics import (
    calculate_z_score,
    rolling_average_deviation,
    ewma_score,
)


class AnomalyDetectionService:

    @staticmethod
    def detect_anomaly(values):

        z_score = calculate_z_score(values)

        rolling_dev = rolling_average_deviation(values)

        ewma_dev = ewma_score(values)

        anomaly_score = (
            abs(z_score) * 0.4
            + abs(rolling_dev) * 0.3
            + abs(ewma_dev) * 0.3
        )

        severity = "LOW"

        if anomaly_score > 250:
            severity = "CRITICAL"

        elif anomaly_score > 150:
            severity = "HIGH"

        elif anomaly_score > 75:
            severity = "MEDIUM"

        return {
            "z_score": round(z_score, 2),
            "rolling_deviation": round(rolling_dev, 2),
            "ewma_deviation": round(ewma_dev, 2),
            "anomaly_score": round(anomaly_score, 2),
            "severity": severity,
        }