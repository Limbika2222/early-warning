import numpy as np
from typing import List, Dict


def calculate_metrics(values: List[int]) -> Dict:
    """
    Professional EWMA-based outbreak analytics.

    - Signal Index = mean of recent 8 weeks
    - Spike Count = EWMA control-limit violations
    - Risk Level = based on signal strength + spike activity

    EWMA detects sustained increases and handles flat baselines safely.
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

    # Convert safely to float
    try:
        arr = np.array(values, dtype=float)
    except Exception:
        return {
            "signal_index": 0,
            "spike_count": 0,
            "risk_level": "Invalid Data",
        }

    if arr.size == 0:
        return {
            "signal_index": 0,
            "spike_count": 0,
            "risk_level": "No Data",
        }

    # --------------------------------------------------
    # 1️⃣ SIGNAL INDEX (last 8 weeks mean)
    # --------------------------------------------------
    recent_window = 8
    recent = arr[-recent_window:] if arr.size >= recent_window else arr
    signal_index = round(float(np.mean(recent)), 2)

    # --------------------------------------------------
    # 2️⃣ EWMA SPIKE DETECTION
    # --------------------------------------------------
    if arr.size < 2:
        spike_count = 0
    else:
        alpha = 0.3  # smoothing factor (professional default)
        L = 2        # control limit multiplier

        # Compute EWMA series
        ewma = np.zeros_like(arr)
        ewma[0] = arr[0]

        for t in range(1, len(arr)):
            ewma[t] = alpha * arr[t] + (1 - alpha) * ewma[t - 1]

        # Sample standard deviation of full history
        sigma = np.std(arr, ddof=1)

        if sigma == 0:
            spike_count = 0
        else:
            # EWMA-adjusted sigma
            sigma_ewma = np.sqrt((alpha / (2 - alpha)) * (sigma ** 2))

            # Upper Control Limit
            ucl = ewma + L * sigma_ewma

            # Only evaluate spikes in recent window
            start_index = max(0, len(arr) - len(recent))
            spike_count = int(np.sum(arr[start_index:] > ucl[start_index:]))

    # --------------------------------------------------
    # 3️⃣ RISK LEVEL CLASSIFICATION
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