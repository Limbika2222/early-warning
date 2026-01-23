from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import trends

app = FastAPI(
    title="Infodemiology Early Warning System API",
    version="1.0.0",
)

# CORS (safe for dev; restrict in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(trends.router)


@app.get("/")
def root():
    return {"status": "API running"}
