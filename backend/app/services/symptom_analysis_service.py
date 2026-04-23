from sqlalchemy.orm import Session
from datetime import date
from collections import defaultdict
import numpy as np

from app.models.google_trends import (
    GoogleTrendsTimeseries,
    GoogleTrendsKeyword,
)
from app.models.symptom_trends import SymptomTrend


# =====================================================
# 🔹 HELPER FUNCTIONS
# =====================================================

def compute_daily_change(values):
    changes = []
    for i, v in enumerate(values):
        if i == 0:
            changes.append(0)
        else:
            changes.append(v - values[i - 1])
    return changes


def compute_ewma(values, alpha=0.3):
    ewma = []
    prev = values[0]

    for v in values:
        current = alpha * v + (1 - alpha) * prev
        ewma.append(current)
        prev = current

    return ewma


def detect_spikes(values):
    if len(values) < 3:
        return [False] * len(values)

    mean = np.mean(values)
    std = np.std(values)
    threshold = mean + 2 * std

    return [v > threshold for v in values]


# =====================================================
# 🔹 MAIN FUNCTION
# =====================================================

def calculate_symptom_growth(db: Session):
    """
    Professional symptom signal processing:
    - growth (trend)
    - change (momentum)
    - ewma (smoothed signal)
    - spike detection

    Returns:
        {
            "fever": {
                "growth": 12.3,
                "momentum": 4.2,
                "spike_count": 2
            }
        }
    """

    results = (
        db.query(
            GoogleTrendsKeyword.keyword_text,
            GoogleTrendsTimeseries.date,
            GoogleTrendsTimeseries.interest_index,
        )
        .join(
            GoogleTrendsTimeseries,
            GoogleTrendsKeyword.id == GoogleTrendsTimeseries.keyword_id,
        )
        .order_by(GoogleTrendsTimeseries.date.asc())
        .all()
    )

    symptom_values = defaultdict(list)

    for keyword, _, interest in results:
        symptom_values[keyword].append(interest)

    final_results = {}

    for symptom, values in symptom_values.items():
        if len(values) < 2:
            continue

        # -------------------------------
        # Growth (long-term trend)
        # -------------------------------
        if len(values) >= 6:
            first_avg = sum(values[:3]) / 3
            last_avg = sum(values[-3:]) / 3
            growth = last_avg - first_avg
        else:
            growth = values[-1] - values[0]

        # -------------------------------
        # Momentum (recent change)
        # -------------------------------
        changes = compute_daily_change(values)
        momentum = changes[-1]

        # -------------------------------
        # EWMA (smoothed signal)
        # -------------------------------
        ewma = compute_ewma(values)

        # -------------------------------
        # Spike detection
        # -------------------------------
        spikes = detect_spikes(values)
        spike_count = sum(spikes)

        # Round values
        growth = round(growth, 2)
        momentum = round(momentum, 2)

        final_results[symptom] = {
            "growth": growth,
            "momentum": momentum,
            "spike_count": spike_count,
        }

        # -------------------------------
        # Store in DB (growth only)
        # -------------------------------
        trend = SymptomTrend(
            symptom=symptom,
            growth_value=growth,
            date_calculated=date.today(),
        )
        db.add(trend)

    db.commit()

    return final_results


# =====================================================
# 🔹 TOP SYMPTOMS
# =====================================================

def get_top_trending_symptoms(db: Session, top_n: int = 5):
    """
    Returns top N symptoms by growth
    """

    results = (
        db.query(SymptomTrend)
        .order_by(SymptomTrend.growth_value.desc())
        .limit(top_n)
        .all()
    )

    return [
        {
            "symptom": r.symptom,
            "interest": r.growth_value,  # keep frontend compatibility
        }
        for r in results
    ]