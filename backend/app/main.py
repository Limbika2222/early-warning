from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import trends

app = FastAPI(
    title="Infodemiology Early Warning System API",
    version="0.1.0",
)

# --- CORS (needed for frontend) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(trends.router)


@app.get("/")
def root():
    return {"status": "API running"}
