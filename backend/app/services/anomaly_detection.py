from statistics import (
    mean,
    stdev,
)

from sqlalchemy.orm import Session

from app.models.alerts import Alert

from app.models.google_trends import (
    GoogleTrendsTimeseries,
    GoogleTrendsKeyword,
    Country,
)

from app.models.reddit_signal import (
    RedditSignal,
)

from app.models.who_outbreaks import (
    WhoOutbreakReport,
)

# =====================================================
# Z SCORE
# =====================================================

def calculate_z_score(
    current,
    historical
):

    if len(historical) < 2:
        return 0

    avg = mean(historical)

    std = stdev(historical)

    if std == 0:
        return 0

    return (
        current - avg
    ) / std

# =====================================================
# EWMA
# =====================================================

def calculate_ewma(
    values,
    alpha=0.3
):

    ewma = values[0]

    for value in values[1:]:

        ewma = (
            alpha * value
        ) + (
            (1 - alpha) * ewma
        )

    return ewma

# =====================================================
# GOOGLE TRENDS ANALYSIS
# =====================================================

def analyze_google_trends(
    db: Session
):

    timeseries = (

        db.query(
            GoogleTrendsTimeseries
        )

        .all()
    )

    grouped = {}

    for row in timeseries:

        keyword = (
            db.query(
                GoogleTrendsKeyword
            )

            .filter(
                GoogleTrendsKeyword.id
                == row.keyword_id
            )

            .first()
        )

        country = (
            db.query(Country)

            .filter(
                Country.id
                == row.country_id
            )

            .first()
        )

        if not keyword or not country:
            continue

        disease = (
            keyword.keyword_text
        )

        country_name = (
            country.name
        )

        key = (
            disease,
            country_name
        )

        grouped.setdefault(
            key,
            []
        ).append(row)

    # =================================================
    # ANALYZE GROUPS
    # =================================================

    for (
        disease,
        country
    ), rows in grouped.items():

        rows.sort(
            key=lambda x: x.date
        )

        values = [
            r.interest_index
            for r in rows
        ]

        if len(values) < 5:
            continue

        current = values[-1]

        historical = values[:-1]

        z_score = calculate_z_score(
            current,
            historical
        )

        ewma = calculate_ewma(
            historical
        )

        anomaly_score = abs(
            z_score
        ) * 20

        max_value = max(values)
        if max_value == 0:
            risk_score = 0
        else:
            risk_score = (
                current / max_value
            ) * 100


        # =============================================
        # TRIGGER ALERT
        # =============================================

        if (
            z_score > 2
            or current > ewma * 1.5
        ):

            severity = "MEDIUM"

            if anomaly_score > 80:

                severity = "CRITICAL"

            elif anomaly_score > 60:

                severity = "HIGH"
            
            existing_alert = (
                db.query(Alert)
                .filter(
                    Alert.disease == disease,
                    Alert.country == country,
                    Alert.source == "Google Trends",
                    Alert.resolved == False,
                )
                .first()
            )

            if existing_alert:
                continue

            alert = Alert(

                disease=disease,

                country=country,

                source="Google Trends",

                risk_score=round(
                    risk_score,
                    2
                ),

                anomaly_score=round(
                    anomaly_score,
                    2
                ),

                outbreak_probability=round(
                    anomaly_score / 100,
                    2
                ),

                severity=severity,

                trend_direction="upward",

                status="active",

                message=(
                    f"Search anomaly detected "
                    f"for {disease}"
                ),

                resolved=False,
            )

            db.add(alert)

    db.commit()

# =====================================================
# REDDIT ANALYSIS
# =====================================================

def analyze_reddit_signals(
    db: Session
):

    signals = (

        db.query(
            RedditSignal
        )

        .all()
    )

    for signal in signals:

        if (
            signal.signal_strength > 80
        ):

            existing_alert = (
                db.query(Alert)
                .filter(
                    Alert.disease == signal.disease,
                    Alert.source == "Reddit",
                    Alert.resolved == False,
                )
                .first()
            )

            if existing_alert:
                continue

            alert = Alert(

                disease=signal.disease,

                country="Unknown",

                source="Reddit",

                risk_score=85,

                anomaly_score=90,

                outbreak_probability=0.88,

                severity="HIGH",

                trend_direction="upward",

                status="active",

                message=(
                    "Reddit symptom spike "
                    "detected"
                ),

                resolved=False,
            )

            db.add(alert)

    db.commit()

# =====================================================
# WHO ANALYSIS
# =====================================================

def analyze_who_outbreaks(
    db: Session
):

    outbreaks = (

        db.query(
            WhoOutbreakReport
        )

        .all()
    )

    for outbreak in outbreaks:

        existing_alert = (
            db.query(Alert)
            .filter(
                Alert.disease == outbreak.disease,
                Alert.country == outbreak.country_name,
                Alert.source == "WHO",
                Alert.resolved == False,
            )
            .first()
        )

        if existing_alert:
            continue

        alert = Alert(

            disease=outbreak.disease,

            country=(
                outbreak.country_name
                or "Unknown"
            ),

            source="WHO",

            risk_score=95,

            anomaly_score=98,

            outbreak_probability=0.97,

            severity="CRITICAL",

            trend_direction="upward",

            status="active",

            message=(
                outbreak.title
            ),

            resolved=False,
        )

        db.add(alert)

    db.commit()

# =====================================================
# MAIN ENGINE
# =====================================================

def run_anomaly_detection(
    db: Session
):

    analyze_google_trends(db)

    analyze_reddit_signals(db)

    analyze_who_outbreaks(db)

    print(
        "✅ Anomaly detection completed"
    )