from fastapi import FastAPI

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

from app.api.ranking_api import (
    router as ranking_router,
)

from app.api.admin_api import (
    router as admin_router
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
# Prediction API (NEW)
# -------------------------------------------------

from app.api.prediction_api import (
    router as prediction_router,
)

# =====================================================
# CREATE FASTAPI APPLICATION
# =====================================================

app = FastAPI(

    title=(
        "Infodemiology Early "
        "Warning System API"
    ),

    version="2.7.0",
)

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
# Prediction API (NEW)
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
# Alerts API
# -------------------------------------------------

app.include_router(
    alert_router,

    prefix="/api/alerts",

    tags=["Alerts"],
)

# -------------------------------------------------
# Ranking API
# -------------------------------------------------

app.include_router(
    ranking_router,

    prefix="/api/ranking",

    tags=["Ranking"],
)

app.include_router(
    admin_router
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
        ],
    }

# =====================================================
# HEALTH
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
        },
    }