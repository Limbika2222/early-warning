from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# -------------------------------------------------
# Import Routers (IMPORTANT: renamed signal → signal_api)
# -------------------------------------------------
from app.api import trends
from app.api import signal_api


# -------------------------------------------------
# Create FastAPI Application
# -------------------------------------------------
app = FastAPI(
    title="Infodemiology Early Warning System API",
    version="1.0.0",
    description="Unified analytics API for Google Trends, Twitter, WHO, and ML-based outbreak detection",
)


# -------------------------------------------------
# CORS Configuration
# -------------------------------------------------
# In development we allow all origins.
# In production you should restrict this.
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")

if ALLOWED_ORIGINS == "*":
    origins = ["*"]
else:
    origins = [origin.strip() for origin in ALLOWED_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------
# Register API Routers
# -------------------------------------------------
app.include_router(trends.router)
app.include_router(signal_api.router)


# -------------------------------------------------
# Root Endpoint
# -------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "API running",
        "service": "Infodemiology Early Warning System",
        "version": "1.0.0",
    }


# -------------------------------------------------
# Health Check Endpoint
# -------------------------------------------------
@app.get("/health")
def health_check():
    return {"health": "ok"}