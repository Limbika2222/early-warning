from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
import pandas as pd

# ✅ CORRECT MODELS (FIXED)
from app.models.google_trends import (
    GoogleTrendsTimeseries,   # ✅ FIXED NAME
    GoogleTrendsKeyword,
    DiseaseRisk,
    Disease,
)


# -------------------------------------------------
# 🔥 MAIN ANALYSIS FUNCTION
# -------------------------------------------------
def compute_disease_risk(db: Session, window_days: int = 7):
    print("🚀 Starting disease risk computation...")

    # -------------------------------------------------
    # 1. LOAD DATA (FIXED QUERY + JOIN)
    # -------------------------------------------------
    rows = (
        db.query(GoogleTrendsTimeseries)
        .join(GoogleTrendsKeyword)
        .all()
    )

    if not rows:
        print("⚠️ No Google Trends data found")
        return []

    # -------------------------------------------------
    # 2. BUILD DATAFRAME (FIXED FIELDS)
    # -------------------------------------------------
    df = pd.DataFrame([{
        "keyword": r.keyword.keyword_text.strip().lower(),   # ✅ FIXED
        "date": r.date,
        "interest": r.interest_index                         # ✅ FIXED
    } for r in rows])

    df["date"] = pd.to_datetime(df["date"])

    print(f"📊 Loaded {len(df)} rows")

    # -------------------------------------------------
    # 3. NORMALIZE PER KEYWORD
    # -------------------------------------------------
    df["normalized"] = df.groupby("keyword")["interest"].transform(
        lambda x: (x - x.min()) / (x.max() - x.min() + 1e-9)
    )

    # -------------------------------------------------
    # 4. TIME WINDOW
    # -------------------------------------------------
    latest_date = df["date"].max()
    cutoff_date = latest_date - timedelta(days=window_days)

    df = df[df["date"] >= cutoff_date]

    print(f"🕒 Using data from {cutoff_date.date()} → {latest_date.date()}")

    # -------------------------------------------------
    # 5. KEYWORD SCORES
    # -------------------------------------------------
    keyword_scores = (
        df.groupby("keyword")["normalized"]
        .mean()
        .reset_index()
        .rename(columns={"normalized": "keyword_score"})
    )

    # -------------------------------------------------
    # 6. LOAD KEYWORD → DISEASE MAPPING (FIXED FIELD)
    # -------------------------------------------------
    mappings = db.query(GoogleTrendsKeyword).all()

    map_df = pd.DataFrame([{
        "keyword": m.keyword_text.strip().lower(),  # ✅ FIXED
        "disease_id": m.disease_id,
        "weight": m.weight if m.weight else 1.0
    } for m in mappings if m.disease_id is not None])

    if map_df.empty:
        print("⚠️ No keyword mappings found")
        return []

    # -------------------------------------------------
    # 7. MERGE
    # -------------------------------------------------
    merged = pd.merge(keyword_scores, map_df, on="keyword", how="inner")

    if merged.empty:
        print("⚠️ No matching keywords after merge")
        return []

    # -------------------------------------------------
    # 8. WEIGHTED SCORING
    # -------------------------------------------------
    merged["weighted_score"] = merged["keyword_score"] * merged["weight"]

    disease_scores = (
        merged.groupby("disease_id")
        .apply(lambda x: x["weighted_score"].sum() / x["weight"].sum())
        .reset_index(name="score")
    )

    # -------------------------------------------------
    # 9. MAP DISEASE NAMES
    # -------------------------------------------------
    diseases = db.query(Disease).all()
    disease_map = {d.id: d.name for d in diseases}

    disease_scores["disease"] = disease_scores["disease_id"].map(disease_map)

    # -------------------------------------------------
    # 10. RISK LEVEL
    # -------------------------------------------------
    def get_risk_level(score):
        if score >= 0.7:
            return "HIGH"
        elif score >= 0.4:
            return "MEDIUM"
        elif score > 0:
            return "LOW"
        else:
            return "NONE"

    disease_scores["risk_level"] = disease_scores["score"].apply(get_risk_level)

    # -------------------------------------------------
    # 11. OUTPUT
    # -------------------------------------------------
    result = disease_scores[["disease", "score", "risk_level"]].to_dict(orient="records")

    print("✅ Disease scoring completed")

    return result


# -------------------------------------------------
# 🔥 STORAGE FUNCTION
# -------------------------------------------------
def store_disease_risk(db: Session, disease_risk_data):
    today = date.today()

    print("🔥 Storing disease risk data...")

    inserted_count = 0
    updated_count = 0

    for item in disease_risk_data:
        disease_name = item["disease"].lower().strip()

        disease = (
            db.query(Disease)
            .filter(Disease.name.ilike(disease_name))
            .first()
        )

        if not disease:
            print(f"[WARNING] Disease not found: {disease_name}")
            continue

        existing = (
            db.query(DiseaseRisk)
            .filter(DiseaseRisk.disease_id == disease.id)
            .filter(DiseaseRisk.date_calculated == today)
            .first()
        )

        score = float(item["score"])

        if existing:
            existing.risk_score = score
            existing.risk_level = item["risk_level"]
            existing.created_at = datetime.utcnow()
            updated_count += 1
        else:
            record = DiseaseRisk(
                disease_id=disease.id,
                disease_name=disease.name,
                risk_score=score,
                risk_level=item["risk_level"],
                date_calculated=today,
                created_at=datetime.utcnow(),
            )
            db.add(record)
            inserted_count += 1

    db.commit()

    print(f"✅ Stored: inserted={inserted_count}, updated={updated_count}")


# -------------------------------------------------
# 🔥 PIPELINE HELPER
# -------------------------------------------------
def run_full_risk_pipeline(db: Session):
    results = compute_disease_risk(db)

    if not results:
        print("⚠️ No results to store")
        return []

    store_disease_risk(db, results)

    return results