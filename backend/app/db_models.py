from sqlalchemy import Column, Integer, String

from app.database import Base


# ==========================================================
# User Model
# ==========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )


# ==========================================================
# Security Analysis Model
# ==========================================================

class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(
        String,
        nullable=False
    )

    risk_level = Column(
        String,
        nullable=False,
        default="Unknown"
    )

    attack_type = Column(
        String,
        nullable=False,
        default="Unknown"
    )

    severity_score = Column(
        Integer,
        nullable=False,
        default=0
    )

    confidence = Column(
        Integer,
        nullable=False,
        default=0
    )

    reasoning = Column(
        String,
        nullable=False,
        default=""
    )

    affected_assets = Column(
        String,
        nullable=False,
        default="[]"
    )

    iocs = Column(
        String,
        nullable=False,
        default="[]"
    )

    summary = Column(
        String,
        nullable=False,
        default=""
    )

    recommendations = Column(
        String,
        nullable=False,
        default="[]"
    )

    next_steps = Column(
        String,
        nullable=False,
        default="[]"
    )