from langgraph.graph import StateGraph, END
from typing import TypedDict

from app.ai.pipelines.rag_pipeline import RAGPipeline


class AgentState(TypedDict):
    query: str
    response: str


rag = RAGPipeline()


def analyze_security(state: AgentState):

    answer = rag.analyze(state["query"])

    return {
        "query": state["query"],
        "response": answer
    }


builder = StateGraph(AgentState)

builder.add_node("SecurityAnalyzer", analyze_security)

builder.set_entry_point("SecurityAnalyzer")

builder.add_edge("SecurityAnalyzer", END)

graph = builder.compile()


if __name__ == "__main__":

    result = graph.invoke(
        {
            "query": "Explain brute force attack."
        }
    )

    print(result["response"])