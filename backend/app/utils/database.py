from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from pathlib import Path
import os

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()

# -------------------------------------------------
# Resolve DB path (SAFE + SIMPLE)
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # backend/

DB_PATH = BASE_DIR / "early_warning.db"

# -------------------------------------------------
# Database URL
# -------------------------------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DB_PATH}"
)

# -------------------------------------------------
# Engine config
# -------------------------------------------------
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False,
)

# -------------------------------------------------
# Session
# -------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# -------------------------------------------------
# Base
# -------------------------------------------------
Base = declarative_base()