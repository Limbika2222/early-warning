import numpy as np
from typing import List, Dict


def calculate_metrics(values: List[int]) -> Dict:
    """
    Calculate outbreak analytics metrics.

    - Signal Index = mean of recent 8 weeks
    - Spike Count = Z-score anomalies in recent window
      (baseline excludes recent values to avoid self-bias)
    - Risk Level = based on signal strength + spike activity
    """

    # --------------------------------------------------
    # 0️⃣ Guard: No Data
    # --------------------------------------------------
    if not values:
        return {
            "signal_index": 0,
            "spike_count": 0,
            "risk_level": "No Data",
        }

    # Ensure numeric float array
    try:
        arr = np.array(values, dtype=float)
    except Exception:
        return {
            "signal_index": 0,
            "spike_count": 0,
            "risk_level": "Invalid Data",
        }

    # --------------------------------------------------
    # 1️⃣ RECENT SIGNAL INDEX (last 8 weeks)
    # --------------------------------------------------
    recent_window = 8

    if arr.size >= recent_window:
        recent = arr[-recent_window:]
    else:
        recent = arr

    signal_index = round(float(np.mean(recent)), 2)

    # --------------------------------------------------
    # 2️⃣ Z-SCORE SPIKE DETECTION
    # --------------------------------------------------
    if arr.size < 2:
        spike_count = 0

    else:
        # Baseline excludes recent window (prevents self-bias)
        if arr.size > recent_window:
            baseline = arr[:-recent_window]
        else:
            baseline = arr

        # Not enough baseline data or zero variance
        if baseline.size < 2 or np.std(baseline) == 0:
            spike_count = 0
        else:
            mean_baseline = np.mean(baseline)

            # Use sample std (ddof=1)
            std_baseline = np.std(baseline, ddof=1)

            if std_baseline == 0:
                spike_count = 0
            else:
                z_scores = (recent - mean_baseline) / std_baseline

                # 2σ threshold
                spike_count = int(np.sum(z_scores > 2))

    # --------------------------------------------------
    # 3️⃣ RISK LEVEL LOGIC
    # --------------------------------------------------
    if signal_index >= 60 or spike_count >= 3:
        risk = "High"
    elif signal_index >= 35 or spike_count >= 1:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "signal_index": signal_index,
        "spike_count": spike_count,
        "risk_level": risk,
    }