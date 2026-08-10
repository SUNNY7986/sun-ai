from typing import List

from pydantic import BaseModel


# ==========================================
# Authentication Models
# ==========================================

class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


# ==========================================
# Log Analysis Request
# ==========================================

class LogRequest(BaseModel):
    log_text: str


# ==========================================
# AI Analysis Response
# ==========================================

class AnalysisResponse(BaseModel):
    risk_level: str
    severity_score: int
    confidence: int

    attack_type: str
    reasoning: str

    affected_assets: List[str]
    iocs: List[str]

    summary: str

    recommendations: List[str]
    next_steps: List[str]