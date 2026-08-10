import json
import re
from typing import Any, Dict

from dotenv import load_dotenv

from app.ai.agents.report_agent import ReportAgent


load_dotenv()

report_agent = ReportAgent()


DEFAULT_RESULT = {
    "risk_level": "Unknown",
    "severity_score": 0,
    "confidence": 0,
    "attack_type": "Unknown",
    "reasoning": "",
    "affected_assets": [],
    "iocs": [],
    "summary": "",
    "recommendations": [],
    "next_steps": [],
}


def clean_response(text: str) -> str:
    """Remove markdown code fences and surrounding whitespace."""
    if not text:
        return ""

    text = str(text).strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def extract_json(text: str):
    """Parse JSON directly or extract the first JSON object from text."""
    if not text:
        return None

    cleaned = clean_response(text)

    try:
        return json.loads(cleaned)
    except (json.JSONDecodeError, TypeError):
        pass

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start != -1 and end > start:
        try:
            return json.loads(cleaned[start:end + 1])
        except (json.JSONDecodeError, TypeError):
            return None

    return None


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def safe_list(value: Any) -> list:
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    if isinstance(value, str):
        value = value.strip()

        if not value:
            return []

        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return parsed
        except (json.JSONDecodeError, TypeError):
            pass

        return [value]

    return [value]


def validate_response(data: Any) -> Dict[str, Any]:
    """Normalize the ReportAgent result to the database/API schema."""

    result = DEFAULT_RESULT.copy()

    if not isinstance(data, dict):
        return result

    result.update({
        key: value
        for key, value in data.items()
        if key in result and value is not None
    })

    risk_level = str(result["risk_level"]).strip().capitalize()

    if risk_level not in {"Low", "Medium", "High", "Critical"}:
        risk_level = "Unknown"

    result["risk_level"] = risk_level

    result["severity_score"] = max(
        0, min(100, safe_int(result["severity_score"]))
    )

    result["confidence"] = max(
        0, min(100, safe_int(result["confidence"]))
    )

    result["attack_type"] = str(result["attack_type"] or "Unknown")
    result["reasoning"] = str(result["reasoning"] or "")
    result["summary"] = str(result["summary"] or "")

    result["affected_assets"] = safe_list(result["affected_assets"])
    result["iocs"] = safe_list(result["iocs"])
    result["recommendations"] = safe_list(result["recommendations"])
    result["next_steps"] = safe_list(result["next_steps"])

    return result


def analyze_security_log(log_text: str) -> Dict[str, Any]:
    """
    Run the existing SUN AI ReportAgent pipeline and return a
    stable response consumed by routes.py and the React frontend.
    """

    if not log_text or not str(log_text).strip():
        return {
            **DEFAULT_RESULT,
            "reasoning": "No security log was provided.",
            "summary": "Security log input was empty.",
            "recommendations": ["Provide a valid security log."],
            "next_steps": ["Submit a security log for analysis."],
        }

    try:
        raw_result = report_agent.generate_report(str(log_text).strip())

        if isinstance(raw_result, str):
            parsed = extract_json(raw_result)
            raw_result = parsed if parsed is not None else {
                "severity": "Unknown",
                "risk_score": 0,
                "threat": "Unknown",
                "analysis": raw_result,
                "recommendations": [],
            }

        if not isinstance(raw_result, dict):
            raw_result = {}

        severity = str(raw_result.get("severity", "")).strip().lower()

        risk_score = max(
            0,
            min(100, safe_int(raw_result.get("risk_score"), 50))
        )

        if severity == "critical":
            risk_level = "Critical"
        elif severity == "high":
            risk_level = "High"
        elif severity == "medium":
            risk_level = "Medium"
        elif severity == "low":
            risk_level = "Low"
        elif risk_score >= 80:
            risk_level = "Critical"
        elif risk_score >= 60:
            risk_level = "High"
        elif risk_score >= 30:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        confidence = max(
            0,
            min(100, safe_int(raw_result.get("confidence"), risk_score))
        )

        reasoning = raw_result.get(
            "analysis",
            raw_result.get("reasoning", "")
        )

        response = {
            "risk_level": risk_level,
            "severity_score": risk_score,
            "confidence": confidence,
            "attack_type": raw_result.get(
                "threat",
                raw_result.get("attack_type", "Unknown")
            ),
            "reasoning": reasoning,
            "affected_assets": raw_result.get("affected_assets", []),
            "iocs": raw_result.get(
                "iocs",
                raw_result.get("indicators", [])
            ),
            "summary": raw_result.get("summary", reasoning),
            "recommendations": raw_result.get("recommendations", []),
            "next_steps": raw_result.get(
                "next_steps",
                [
                    "Review the incident.",
                    "Investigate affected systems.",
                    "Apply the recommended mitigations.",
                    "Continue monitoring for suspicious activity.",
                ],
            ),
        }

        return validate_response(response)

    except Exception as exc:
        return {
            **DEFAULT_RESULT,
            "reasoning": str(exc),
            "summary": "AI pipeline failed while analyzing the incident.",
            "recommendations": [
                "Check the backend logs.",
                "Verify the ReportAgent configuration.",
                "Verify the Groq API configuration.",
                "Retry the analysis.",
            ],
            "next_steps": [
                "Inspect the backend error message.",
                "Verify the AI agent configuration.",
                "Restart the backend if necessary.",
            ],
        }