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

# ✅ ADD THIS
from app.api.ranking_api import router as ranking_router

# -------------------------------------------------
# Create FastAPI Application
# -------------------------------------------------
app = FastAPI(
    title="Infodemiology Early Warning System API",
    version="2.4.0",
)

# -------------------------------------------------
# 🚀 CORS (IMPORTANT FOR FRONTEND)
# -------------------------------------------------
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://5173-firebase-early-warning-1772198111524.cluster-fdkw7vjj7bgguspe3fbbc25tra.cloudworkstations.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Register Routers
# -------------------------------------------------

# Upload
app.include_router(upload_router)

# Existing
app.include_router(trends.router)
app.include_router(signal_api.router)

# Analysis
app.include_router(
    analysis_router,
    prefix="/analysis",
    tags=["Analysis"]
)

# Alerts
app.include_router(
    alert_router,
    prefix="/alerts",
    tags=["Alerts"]
)

# 🔥 ADD THIS (VERY IMPORTANT)
app.include_router(ranking_router)

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