from langgraph.graph import StateGraph, END
from typing import TypedDict

from app.ai.agents.security_agent import analyze_security
from app.ai.agents.threat_classifier import ThreatClassifier
from app.ai.agents.severity_agent import SeverityAgent


class AgentState(TypedDict):
    query: str
    response: str
    threat: str
    severity: str


classifier = ThreatClassifier()
severity_agent = SeverityAgent()


def security_node(state: AgentState):
    return analyze_security(state)


def threat_node(state: AgentState):
    threat = classifier.classify(state["query"])

    return {
        **state,
        "threat": threat
    }


def severity_node(state: AgentState):
    severity = severity_agent.predict_severity(state["query"])

    return {
        **state,
        "severity": severity
    }


builder = StateGraph(AgentState)

builder.add_node("Security", security_node)
builder.add_node("Threat", threat_node)
builder.add_node("Severity", severity_node)

builder.set_entry_point("Security")

builder.add_edge("Security", "Threat")
builder.add_edge("Threat", "Severity")
builder.add_edge("Severity", END)

graph = builder.compile()


if __name__ == "__main__":

    result = graph.invoke(
        {
            "query": "Multiple failed login attempts from one IP address."
        }
    )

    print("\nAI RESPONSE")
    print(result["response"])

    print("\nTHREAT")
    print(result["threat"])

    print("\nSEVERITY")
    print(result["severity"])