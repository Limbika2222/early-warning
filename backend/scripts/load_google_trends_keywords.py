from sqlalchemy.orm import sessionmaker
from pathlib import Path

from app.utils.database import engine
from app.models.google_trends import Disease, GoogleTrendsKeyword

Session = sessionmaker(bind=engine)
db = Session()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
KEYWORDS_FILE = PROJECT_ROOT / "docs" / "google_trends_queries.md"

def detect_language(keyword: str) -> str:
    try:
        keyword.encode("ascii")
        return "en"
    except UnicodeEncodeError:
        return "hi"

def parse_keywords(md_path: Path):
    current_disease = None
    keywords = []

    with open(md_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line.startswith("## "):
                current_disease = line.replace("## ", "").strip()
            elif line.startswith("- ") and current_disease:
                keyword = line.replace("- ", "").strip()
                keywords.append((current_disease, keyword))

    return keywords

def load_keywords():
    keyword_pairs = parse_keywords(KEYWORDS_FILE)

    for disease_name, keyword_text in keyword_pairs:
        disease = (
            db.query(Disease)
            .filter(Disease.name == disease_name)
            .first()
        )

        if not disease:
            print(f"⚠ Disease not found: {disease_name}")
            continue

        language = detect_language(keyword_text)
        category = "disease" if disease_name.lower() in keyword_text.lower() else "symptom"

        record = GoogleTrendsKeyword(
            disease_id=disease.id,
            keyword_text=keyword_text,
            language=language,
            category=category,
            weight=1.5 if category == "symptom" else 1.0,
            active=True,
        )

        db.add(record)

    db.commit()
    print("✅ Google Trends keywords loaded successfully")

if __name__ == "__main__":
    load_keywords()
