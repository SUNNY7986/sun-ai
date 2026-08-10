from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.db_models import Base
from app.routes import router


# ==========================================================
# Environment
# ==========================================================

load_dotenv()


# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(
    title="SUN AI",
    description="AI-Powered Cybersecurity Threat Analysis Platform",
    version="2.0.0",
)


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# Database
# ==========================================================

Base.metadata.create_all(bind=engine)


# ==========================================================
# Routes
# ==========================================================

app.include_router(router)


# ==========================================================
# Root
# ==========================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to SUN AI",
        "status": "Backend Running",
        "version": "2.0.0",
    }


# ==========================================================
# Health Check
# ==========================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "database": "connected",
        "ai": "Groq",
    }