from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# -------------------------------------------------
# Import Routers
# -------------------------------------------------

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

# Reddit Signal API
from app.api.reddit_signal_api import (
    router as reddit_router,
)

# -------------------------------------------------
# Create FastAPI Application
# -------------------------------------------------

app = FastAPI(
    title="Infodemiology Early Warning System API",
    version="2.5.0",
)

# -------------------------------------------------
# CORS
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Register Routers
# -------------------------------------------------

# Upload routes
# NOTE:
# upload_api.py likely has NO internal prefix
app.include_router(
    upload_router,
    prefix="/api/trends",
    tags=["Upload"],
)

# -------------------------------------------------
# Trends routes
# IMPORTANT:
# trends.py ALREADY contains:
# prefix="/api/trends"
# so DO NOT double-prefix here
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
    reddit_router,
    prefix="/api",
    tags=["Reddit"],
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

# -------------------------------------------------
# Root
# -------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "API running"
    }

# -------------------------------------------------
# Health
# -------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "health": "ok"
    }