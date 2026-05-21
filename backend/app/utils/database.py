from sqlalchemy import create_engine

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
)

from dotenv import load_dotenv

from pathlib import Path

import os

# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()

# =====================================================
# BASE DIRECTORY
# backend/
# =====================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)

# =====================================================
# SQLITE DATABASE PATH
# =====================================================

DB_PATH = (
    BASE_DIR
    / "early_warning.db"
)

# =====================================================
# DATABASE URL
# =====================================================

DATABASE_URL = os.getenv(

    "DATABASE_URL",

    f"sqlite:///{DB_PATH}"
)

# =====================================================
# SQLITE CONFIG
# =====================================================

connect_args = (

    {
        "check_same_thread": False
    }

    if DATABASE_URL.startswith(
        "sqlite"
    )

    else {}
)

# =====================================================
# ENGINE
# =====================================================

engine = create_engine(

    DATABASE_URL,

    connect_args=connect_args,

    echo=False,
)

# =====================================================
# SESSION
# =====================================================

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine,
)

# =====================================================
# BASE MODEL
# =====================================================

Base = declarative_base()

# =====================================================
# INIT DATABASE
# =====================================================

def init_db():

    """
    Register all models
    and create tables
    """

    # -------------------------------------------------
    # IMPORT ALL MODELS
    # -------------------------------------------------

    import app.models.google_trends

    import app.models.reddit_signal

    import app.models.who_outbreaks

    import app.models.alerts

    # -------------------------------------------------
    # CREATE TABLES
    # -------------------------------------------------

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "✅ Database tables created"
    )

# =====================================================
# AUTO INITIALIZE
# =====================================================

init_db()