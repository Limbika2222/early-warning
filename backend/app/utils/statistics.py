import numpy as np
import pandas as pd


def calculate_z_score(values):
    mean = np.mean(values)
    std = np.std(values)

    if std == 0:
        return 0

    latest = values[-1]

    return (latest - mean) / std


def rolling_average_deviation(values, window=7):
    series = pd.Series(values)

    rolling_mean = series.rolling(window=window).mean()

    latest = series.iloc[-1]
    baseline = rolling_mean.iloc[-2]

    if baseline == 0 or pd.isna(baseline):
        return 0

    deviation = ((latest - baseline) / baseline) * 100

    return deviation


def ewma_score(values, span=7):
    series = pd.Series(values)

    ewma = series.ewm(span=span).mean()

    latest = series.iloc[-1]
    expected = ewma.iloc[-2]

    if expected == 0:
        return 0

    return ((latest - expected) / expected) * 100