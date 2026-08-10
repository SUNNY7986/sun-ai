from datetime import datetime

from app.ai.agents.security_agent import analyze_security
from app.ai.agents.threat_classifier import ThreatClassifier
from app.ai.agents.severity_agent import SeverityAgent
from app.ai.agents.recommendation_agent import RecommendationAgent
from app.ai.agents.mitre_agent import MitreAgent
from app.ai.agents.risk_score_agent import RiskScoreAgent


class ReportAgent:

    def __init__(self):
        self.classifier = ThreatClassifier()
        self.severity = SeverityAgent()
        self.recommender = RecommendationAgent()
        self.mitre = MitreAgent()
        self.risk = RiskScoreAgent()

    def generate_report(self, incident):

        security = analyze_security(
            {
                "query": incident,
                "response": ""
            }
        )

        threat = self.classifier.classify(incident)

        severity = self.severity.predict_severity(incident)

        risk_score = self.risk.calculate_score(severity)

        recommendations = self.recommender.recommend(threat)

        mitre = self.mitre.get_mapping(threat)

        # -----------------------------------------
        # Convert new AI output to old frontend format
        # -----------------------------------------

        if isinstance(severity, str):
            risk_level = severity.capitalize()
        elif risk_score >= 80:
            risk_level = "High"
        elif risk_score >= 50:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        confidence = min(95, max(60, risk_score))

        return {

            # -------- Old frontend fields --------

            "risk_level": risk_level,
            "attack_type": threat,
            "severity_score": risk_score,
            "confidence": confidence,
            "reasoning": security["response"],
            "affected_assets": [],
            "iocs": [],
            "summary": security["response"],
            "recommendations": recommendations,
            "next_steps": [
                "Review the incident.",
                "Investigate affected systems.",
                "Apply recommended mitigations."
            ],

            # -------- New AI fields --------

            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "incident": incident,
            "threat": threat,
            "severity": severity,
            "risk_score": risk_score,
            "mitre": {
                "technique": mitre["technique"],
                "tactic": mitre["tactic"]
            },
            "analysis": security["response"]
        }


if __name__ == "__main__":

    agent = ReportAgent()

    result = agent.generate_report(
        "Multiple failed login attempts detected from one IP address."
    )

    print(result)