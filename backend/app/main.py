from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# -------------------------------------------------
# Import Routers
# -------------------------------------------------
from app.api import trends
from app.api import signal_api
from app.api.upload_api import router as upload_router
from app.api.analysis_api import router as analysis_router
from app.api.alert_api import router as alert_router
from app.api.ranking_api import router as ranking_router

# -------------------------------------------------
# Create FastAPI Application
# -------------------------------------------------
app = FastAPI(
    title="Infodemiology Early Warning System API",
    version="2.4.0",
)

# -------------------------------------------------
# 🚀 CORS (SIMPLE + RELIABLE)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Register Routers (FIXED)
# -------------------------------------------------

# Upload (CSV, history)
app.include_router(
    upload_router,
    prefix="/api/trends",
    tags=["Upload"]
)

# Trends
app.include_router(
    trends.router,
    prefix="/api/trends",
    tags=["Trends"]
)

# ✅ FIXED SIGNAL ROUTE (IMPORTANT)
app.include_router(
    signal_api.router,
    prefix="/api",   # 🔥 FIX HERE
    tags=["Signal"]
)

# Analysis
app.include_router(
    analysis_router,
    prefix="/api/analysis",
    tags=["Analysis"]
)

# Alerts
app.include_router(
    alert_router,
    prefix="/api/alerts",
    tags=["Alerts"]
)

# Ranking
app.include_router(
    ranking_router,
    prefix="/api/ranking",
    tags=["Ranking"]
)

# -------------------------------------------------
# Root
# -------------------------------------------------
@app.get("/")
def root():
    return {"status": "API running"}

# -------------------------------------------------
# Health
# -------------------------------------------------
@app.get("/health")
def health_check():
    return {"health": "ok"}