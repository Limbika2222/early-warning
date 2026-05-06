from sqlalchemy.orm import Session

from app.utils.database import (
    SessionLocal,
)

from app.models.google_trends import (
    GoogleTrendsKeyword,
    GoogleTrendsTimeseries,
    Disease,
    Country,
)

from datetime import (
    datetime,
    date,
)

# =====================================================
# COUNTRY LOOKUP
# =====================================================

def get_country_by_iso2(
    iso2: str
):
    db: Session = SessionLocal()

    try:

        return (
            db.query(Country)
            .filter(
                Country.iso2
                == iso2.upper()
            )
            .first()
        )

    finally:

        db.close()

# =====================================================
# DISEASE INFERENCE
# =====================================================

def infer_disease(
    keyword: str,
    db: Session,
):
    keyword = (
        keyword.lower().strip()
    )

    mapping = {

        "COVID-19": [
            "fever",
            "cough",
            "fatigue",
            "loss of smell",
            "shortness of breath",
        ],

        "Influenza": [
            "fever",
            "cough",
            "chills",
            "sore throat",
        ],

        "Dengue": [
            "fever",
            "skin rash",
            "joint pain",
        ],

        "Malaria": [
            "fever",
            "chills",
            "sweating",
        ],

        "Typhoid": [
            "fever",
            "abdominal pain",
            "weakness",
        ],

        "Pneumonia": [
            "cough",
            "shortness of breath",
        ],

        "Food Poisoning": [
            "vomiting",
            "diarrhea",
        ],

        "Tuberculosis": [
            "cough",
            "weight loss",
        ],

        "Asthma": [
            "shortness of breath",
            "wheezing",
        ],

        "Migraine": [
            "headache",
            "nausea",
        ],
    }

    for (
        disease_name,
        symptoms,
    ) in mapping.items():

        if keyword in symptoms:

            disease = (
                db.query(Disease)
                .filter(
                    Disease.name
                    == disease_name
                )
                .first()
            )

            if disease:

                return disease.id

    return None

# =====================================================
# STORE DATA
# =====================================================

def store_google_trends_data(
    parsed_rows,
    keyword_text,
    country_id,
    upload_id,
):
    db: Session = SessionLocal()

    try:

        keyword_text = (
            keyword_text
            .lower()
            .strip()
        )

        print(
            f"\n🔥 [STORE] "
            f"Processing keyword: "
            f"{keyword_text}"
        )

        # -------------------------------------------------
        # FIND OR CREATE KEYWORD
        # -------------------------------------------------

        keyword = (
            db.query(
                GoogleTrendsKeyword
            )
            .filter(
                GoogleTrendsKeyword.keyword_text
                == keyword_text
            )
            .first()
        )

        if not keyword:

            print(
                f"⚠️ Creating "
                f"new keyword: "
                f"{keyword_text}"
            )

            disease_id = (
                infer_disease(
                    keyword_text,
                    db,
                )
            )

            keyword = (
                GoogleTrendsKeyword(
                    keyword_text=
                        keyword_text,

                    disease_id=
                        disease_id,

                    active=True,
                )
            )

            db.add(keyword)

            db.commit()

            db.refresh(keyword)

        inserted_count = 0

        # -------------------------------------------------
        # INSERT ROWS
        # -------------------------------------------------

        for row in parsed_rows:

            try:

                if (
                    "date" not in row
                    or "interest" not in row
                ):
                    continue

                raw_date = row["date"]

                # -------------------------------------------------
                # DATE HANDLING
                # -------------------------------------------------

                if isinstance(
                    raw_date,
                    datetime,
                ):

                    date_obj = (
                        raw_date.date()
                    )

                elif isinstance(
                    raw_date,
                    date,
                ):

                    date_obj = raw_date

                elif isinstance(
                    raw_date,
                    str,
                ):

                    date_obj = (
                        datetime.strptime(
                            raw_date,
                            "%Y-%m-%d",
                        ).date()
                    )

                else:

                    raise ValueError(
                        "Invalid date type: "
                        f"{type(raw_date)}"
                    )

                interest = int(
                    row["interest"]
                )

                ts = (
                    GoogleTrendsTimeseries(
                        keyword_id=
                            keyword.id,

                        country_id=
                            country_id,

                        date=date_obj,

                        interest_index=
                            interest,

                        upload_id=
                            upload_id,
                    )
                )

                db.add(ts)

                inserted_count += 1

            except Exception as row_error:

                print(
                    f"[ROW ERROR] "
                    f"{row_error}"
                )

                continue

        db.commit()

        print(
            f"✅ [RESULT] "
            f"{keyword_text}: "
            f"inserted={inserted_count}"
        )

        return inserted_count

    except Exception as e:

        db.rollback()

        print(
            f"❌ [ERROR] "
            f"Failed storing data: {e}"
        )

        return 0

    finally:

        db.close()

# =====================================================
# FETCH DATA BY KEYWORD
# =====================================================

def fetch_google_trends_by_keyword(

    keyword,

    # 🌍 OPTIONAL
    country_id=None,

    start_date="",

    end_date="",
):
    db: Session = SessionLocal()

    try:

        keyword = (
            keyword.lower().strip()
        )

        query = (
            db.query(
                GoogleTrendsTimeseries,
                GoogleTrendsKeyword,
            )
            .join(
                GoogleTrendsKeyword,
                GoogleTrendsTimeseries.keyword_id
                == GoogleTrendsKeyword.id,
            )
            .filter(
                GoogleTrendsKeyword.keyword_text
                == keyword
            )
        )

        # -------------------------------------------------
        # 🌍 GEO FILTER
        # -------------------------------------------------

        # ONLY apply filter
        # when specific country selected

        if country_id is not None:

            query = query.filter(
                GoogleTrendsTimeseries.country_id
                == country_id
            )

        else:

            print(
                "🌍 GLOBAL FETCH MODE"
            )

        # -------------------------------------------------
        # DATE FILTERS
        # -------------------------------------------------

        if start_date:

            query = query.filter(
                GoogleTrendsTimeseries.date
                >= start_date
            )

        if end_date:

            query = query.filter(
                GoogleTrendsTimeseries.date
                <= end_date
            )

        results = (
            query
            .order_by(
                GoogleTrendsTimeseries.date
            )
            .all()
        )

        print(
            f"📊 FETCHED "
            f"{len(results)} rows "
            f"for keyword={keyword}"
        )

        return [

            {
                "date":
                    ts.date.strftime(
                        "%Y-%m-%d"
                    ),

                "value":
                    ts.interest_index,

                "keyword":
                    kw.keyword_text,
            }

            for ts, kw in results
        ]

    finally:

        db.close()

# =====================================================
# FETCH KEYWORDS FOR DISEASE
# =====================================================

def fetch_keywords_for_disease(
    disease_id
):
    db: Session = SessionLocal()

    try:

        results = (
            db.query(
                GoogleTrendsKeyword.keyword_text
            )
            .filter(
                GoogleTrendsKeyword.disease_id
                == disease_id
            )
            .filter(
                GoogleTrendsKeyword.active
                == True
            )
            .all()
        )

        return [

            r[0]
            .lower()
            .strip()

            for r in results
        ]

    finally:

        db.close()