from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
import pandas as pd

from app.models.google_trends import (
    GoogleTrendsTimeseries,
    GoogleTrendsKeyword,
    DiseaseRisk,
)

# -------------------------------------------------
# DISEASE → SYMPTOMS + WEIGHTS
# -------------------------------------------------
DISEASE_SYMPTOMS = {
    "Influenza": {
        "fever": 0.8,
        "cough": 1.2,
        "chills": 1.8,
        "sore throat": 1.3,
    },
    "Dengue": {
        "fever": 1.2,
        "rash": 2.0,
        "joint pain": 1.8,
    },
    "Malaria": {
        "fever": 1.5,
        "chills": 2.0,
        "fatigue": 1.0,
    },
    "Typhoid": {
        "fever": 1.2,
        "abdominal pain": 1.8,
    },
    "Pneumonia": {
        "cough": 1.2,
        "shortness of breath": 2.0,
    },
    "Tuberculosis": {
        "cough": 1.2,
        "weight loss": 2.0,
    },
    "Common Cold": {
        "runny nose": 1.5,
        "sore throat": 1.2,
    },
    "Migraine": {
        "headache": 2.5,
    },
}

# -------------------------------------------------
# KEYWORD → DISEASE MATCH
# -------------------------------------------------
def map_keyword(keyword: str):
    keyword = keyword.lower()
    matches = []

    for disease, symptoms in DISEASE_SYMPTOMS.items():
        for symptom, weight in symptoms.items():
            if symptom in keyword:
                matches.append((disease, weight))
                break

    return matches


# -------------------------------------------------
# 🔥 MAIN FUNCTION (FIXED)
# -------------------------------------------------
def compute_disease_risk(
    db: Session,
    end_date: date | None = None,
    window_days: int = 7
):
    print("🚀 Starting disease risk computation...")

    # -------------------------------------------------
    # 🔥 STEP 1: FIND REAL MAX DATE IN DB
    # -------------------------------------------------
    max_date = db.query(
        GoogleTrendsTimeseries.date
    ).order_by(
        GoogleTrendsTimeseries.date.desc()
    ).first()

    if not max_date:
        print("❌ No data in DB")
        return []

    max_date = max_date[0]

    # -------------------------------------------------
    # 🔥 STEP 2: USE SAFE END DATE
    # -------------------------------------------------
    if end_date is None or end_date > max_date:
        end_date = max_date

    start_date = end_date - timedelta(days=window_days)

    print(f"📅 Using window: {start_date} → {end_date}")

    # -------------------------------------------------
    # 🔥 STEP 3: FETCH DATA
    # -------------------------------------------------
    rows = (
        db.query(
            GoogleTrendsTimeseries,
            GoogleTrendsKeyword,
        )
        .join(
            GoogleTrendsKeyword,
            GoogleTrendsTimeseries.keyword_id == GoogleTrendsKeyword.id
        )
        .filter(
            GoogleTrendsTimeseries.date >= start_date,
            GoogleTrendsTimeseries.date <= end_date
        )
        .all()
    )

    # -------------------------------------------------
    # 🔥 FALLBACK IF TOO SMALL
    # -------------------------------------------------
    if len(rows) < 20:
        print("⚠️ Sparse data → expanding window")

        rows = (
            db.query(
                GoogleTrendsTimeseries,
                GoogleTrendsKeyword,
            )
            .join(
                GoogleTrendsKeyword,
                GoogleTrendsTimeseries.keyword_id == GoogleTrendsKeyword.id
            )
            .all()
        )

    if not rows:
        print("❌ No data found")
        return []

    # -------------------------------------------------
    # BUILD DATA
    # -------------------------------------------------
    data = []

    for ts, kw in rows:
        keyword = kw.keyword_text.lower().strip()
        matches = map_keyword(keyword)

        for disease, weight in matches:
            data.append({
                "disease": disease,
                "keyword": keyword,
                "weight": weight,
                "date": ts.date,
                "interest": ts.interest_index,
            })

    df = pd.DataFrame(data)

    if df.empty:
        print("⚠️ No mapped symptoms")
        return []

    df["date"] = pd.to_datetime(df["date"])

    # -------------------------------------------------
    # 🔥 FIX NORMALIZATION (CRITICAL)
    # -------------------------------------------------
    def safe_normalize(x):
        if x.max() == x.min():
            return x / (x.max() + 1e-9)
        return (x - x.min()) / (x.max() - x.min())

    df["normalized"] = df.groupby("keyword")["interest"].transform(safe_normalize)

    # -------------------------------------------------
    # WEIGHTED SCORE
    # -------------------------------------------------
    df["weighted_score"] = df["normalized"] * df["weight"]

    disease_scores = (
        df.groupby("disease")["weighted_score"]
        .sum()
        .reset_index()
    )

    results = []

    for _, row in disease_scores.iterrows():
        score = row["weighted_score"]

        results.append({
            "disease": row["disease"],
            "score": round(score, 3),
            "risk_level": (
                "HIGH" if score >= 3.5 else
                "MEDIUM" if score >= 1.5 else
                "LOW"
            ),
        })

    print("🔥 FINAL DISEASE RANKING:", results)

    return sorted(results, key=lambda x: x["score"], reverse=True)


# -------------------------------------------------
# STORE
# -------------------------------------------------
def store_disease_risk(
    db: Session,
    disease_risk_data,
    calculation_date: date
):
    for item in disease_risk_data:
        existing = db.query(DiseaseRisk).filter(
            DiseaseRisk.disease_name == item["disease"],
            DiseaseRisk.date_calculated == calculation_date
        ).first()

        if existing:
            existing.risk_score = item["score"]
            existing.risk_level = item["risk_level"]
        else:
            db.add(DiseaseRisk(
                disease_name=item["disease"],
                risk_score=item["score"],
                risk_level=item["risk_level"],
                date_calculated=calculation_date,
                created_at=datetime.utcnow()
            ))

    db.commit()


# -------------------------------------------------
# PIPELINE
# -------------------------------------------------
def run_full_risk_pipeline(
    db: Session,
    analysis_date: date | None = None
):
    if analysis_date is None:
        analysis_date = date.today()

    results = compute_disease_risk(
        db,
        end_date=analysis_date
    )

    if results:
        store_disease_risk(
            db,
            results,
            calculation_date=analysis_date
        )

    return results