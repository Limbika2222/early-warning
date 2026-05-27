class RiskScoringEngine:

    @staticmethod
    def calculate_risk(
        google_score,
        reddit_score,
        who_score,
        prediction_confidence,
    ):

        outbreak_probability = (
            google_score * 0.30
            + reddit_score * 0.25
            + who_score * 0.25
            + prediction_confidence * 0.20
        )

        severity_score = outbreak_probability * 100

        return {
            "outbreak_probability": round(outbreak_probability, 2),
            "severity_score": round(severity_score, 2),
        }