from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# ==========================================================
# Database Configuration
# ==========================================================

DATABASE_URL = "sqlite:///./sun_ai.db"


# ==========================================================
# Database Engine
# ==========================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


# ==========================================================
# Session
# ==========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ==========================================================
# Base Model
# ==========================================================

Base = declarative_base()