from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.agents.report_agent import ReportAgent


router = APIRouter(
    prefix="/analyze",
    tags=["AI Analysis"]
)


class IncidentRequest(BaseModel):
    incident: str


report_agent = ReportAgent()


@router.post("/")
def analyze_incident(request: IncidentRequest):

    result = report_agent.generate_report(request.incident)

    return {
        "success": True,
        "data": result
    }