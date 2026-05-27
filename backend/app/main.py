from fastapi import FastAPI
from app.services.scheduler import (
    start_scheduler
)

from fastapi.middleware.cors import (
    CORSMiddleware,
)

# =====================================================
# IMPORT ROUTERS
# =====================================================

from app.api import trends
from app.api import signal_api

from app.api.upload_api import (
    router as upload_router,
)

from app.api.analysis_api import (
    router as analysis_router,
)

from app.api.alert_api import (
    router as alert_router,
)

from app.api.alerts import (
    router as alerts_router,
)

from app.api.ranking_api import (
    router as ranking_router,
)

from app.api.admin_api import (
    router as admin_router,
)

from app.api.auth_api import (
    router as auth_router,
)

from app.api.anomaly_api import (
    router as anomaly_router
)

from app.api.reports_api import (
    router as reports_router
)

from app.api.report_history_api import (
    router as report_history_router
)

from app.api.report_download_api import (
    router as report_download_router
)

from app.api.report_preview_api import (
    router as report_preview_router
)

# -------------------------------------------------
# Reddit Signal API
# -------------------------------------------------

from app.api.reddit_signal_api import (
    router as reddit_router,
)

# -------------------------------------------------
# WHO API
# -------------------------------------------------

from app.api.who_api import (
    router as who_router,
)

# -------------------------------------------------
# Prediction API
# -------------------------------------------------

from app.api.prediction_api import (
    router as prediction_router,
)

# =====================================================
# DATABASE INIT
# =====================================================

from app.utils.database import (
    init_db,
)

# =====================================================
# INITIALIZE DATABASE
# =====================================================

init_db()

# =====================================================
# CREATE FASTAPI APPLICATION
# =====================================================

app = FastAPI(

    title=(
        "Infodemiology Early Warning System API"
    ),

    version="2.7.0",
)

start_scheduler()

# =====================================================
# CORS
# =====================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# =====================================================
# REGISTER ROUTERS
# =====================================================

# -------------------------------------------------
# Upload Routes
# -------------------------------------------------

app.include_router(

    upload_router,

    prefix="/api/trends",

    tags=["Upload"],
)

# -------------------------------------------------
# Trends Routes
# -------------------------------------------------

app.include_router(
    trends.router
)

# -------------------------------------------------
# Signal API
# -------------------------------------------------

app.include_router(

    signal_api.router,

    prefix="/api",

    tags=["Signal"],
)

# -------------------------------------------------
# Reddit Signal API
# -------------------------------------------------

app.include_router(
    reddit_router
)

# -------------------------------------------------
# WHO API
# -------------------------------------------------

app.include_router(
    who_router
)

# -------------------------------------------------
# Prediction API
# -------------------------------------------------

app.include_router(
    prediction_router
)

# -------------------------------------------------
# Analysis API
# -------------------------------------------------

app.include_router(

    analysis_router,

    prefix="/api/analysis",

    tags=["Analysis"],
)

# -------------------------------------------------
# Existing Alert API
# -------------------------------------------------

app.include_router(

    alert_router,

    prefix="/api/alerts",

    tags=["Alerts"],
)

# -------------------------------------------------
# NEW Alerts & Anomalies API
# -------------------------------------------------

app.include_router(
    alerts_router
)

app.include_router(
    anomaly_router
)

# -------------------------------------------------
# Ranking API
# -------------------------------------------------

app.include_router(

    ranking_router,

    prefix="/api/ranking",

    tags=["Ranking"],
)

# -------------------------------------------------
# Admin API
# -------------------------------------------------

app.include_router(
    admin_router
)

# -------------------------------------------------
# Auth API
# -------------------------------------------------

app.include_router(
    auth_router
)

app.include_router(
    reports_router
)

app.include_router(
    report_history_router
)

app.include_router(
    report_download_router
)

app.include_router(
    report_preview_router
)


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():

    return {

        "status":
            "API running",

        "version":
            "2.7.0",

        "services": [

            "google_trends",

            "reddit",

            "who",

            "prediction_engine",

            "alerts_anomalies",
        ],
    }

# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
def health_check():

    return {

        "health":
            "ok",

        "services": {

            "google_trends": True,

            "reddit": True,

            "who": True,

            "prediction_engine": True,

            "alerts_anomalies": True,
        },
    }
