import numpy as np
from typing import List, Dict


def analyze_trends(values: List[int], dates: List[str]) -> Dict:
    """
    Professional EWMA-based outbreak analytics.

    Returns:
    - Per-date anomaly metadata
    - Signal Index
    - Spike Count (recent window)
    - Momentum Percent (4-week growth)
    - Risk Level
    """

    # --------------------------------------------------
    # 0️⃣ Guard: No Data
    # --------------------------------------------------
    if not values or not dates:
        return {
            "trend_data": [],
            "signal_index": 0,
            "spike_count": 0,
            "momentum_percent": 0,
            "risk_level": "No Data",
        }

    try:
        arr = np.array(values, dtype=float)
    except Exception:
        return {
            "trend_data": [],
            "signal_index": 0,
            "spike_count": 0,
            "momentum_percent": 0,
            "risk_level": "Invalid Data",
        }

    alpha = 0.3
    L = 2
    recent_window = 8

    # --------------------------------------------------
    # 1️⃣ EWMA Calculation
    # --------------------------------------------------
    ewma = np.zeros_like(arr)
    ewma[0] = arr[0]

    for t in range(1, len(arr)):
        ewma[t] = alpha * arr[t] + (1 - alpha) * ewma[t - 1]

    sigma = np.std(arr, ddof=1) if len(arr) > 1 else 0

    if sigma == 0:
        sigma_ewma = 0
    else:
        sigma_ewma = np.sqrt((alpha / (2 - alpha)) * (sigma ** 2))

    ucl = ewma + L * sigma_ewma

    # --------------------------------------------------
    # 2️⃣ Build Per-Date Metadata
    # --------------------------------------------------
    trend_data = []

    for i in range(len(arr)):
        is_spike = False
        if sigma_ewma > 0 and arr[i] > ucl[i]:
            is_spike = True

        trend_data.append({
            "date": dates[i],
            "value": float(arr[i]),
            "ewma": round(float(ewma[i]), 2),
            "ucl": round(float(ucl[i]), 2),
            "is_spike": is_spike,
        })

    # --------------------------------------------------
    # 3️⃣ Spike Count (recent window only)
    # --------------------------------------------------
    start_index = max(0, len(arr) - recent_window)
    spike_count = sum(
        1 for i in range(start_index, len(arr))
        if trend_data[i]["is_spike"]
    )

    # --------------------------------------------------
    # 4️⃣ Signal Index (recent mean)
    # --------------------------------------------------
    recent_values = arr[-recent_window:] if len(arr) >= recent_window else arr
    signal_index = round(float(np.mean(recent_values)), 2)

    # --------------------------------------------------
    # 5️⃣ Momentum Detection (4-week growth)
    # --------------------------------------------------
    momentum_percent = 0

    if len(arr) >= 8:
        last4 = np.mean(arr[-4:])
        prev4 = np.mean(arr[-8:-4])

        if prev4 > 0:
            momentum_percent = round(
                ((last4 - prev4) / prev4) * 100,
                2
            )

    # --------------------------------------------------
    # 6️⃣ Risk Classification
    # --------------------------------------------------
    if signal_index >= 60 or spike_count >= 3:
        risk = "High"
    elif signal_index >= 35 or spike_count >= 1 or momentum_percent > 40:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "trend_data": trend_data,
        "signal_index": signal_index,
        "spike_count": spike_count,
        "momentum_percent": momentum_percent,
        "risk_level": risk,
    }