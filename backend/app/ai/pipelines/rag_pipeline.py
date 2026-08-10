from app.ai.rag.retriever import Retriever
from app.ai.llm.llm_service import LLMService


class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = LLMService()

    def analyze(self, query: str):

        results = self.retriever.retrieve(query)

        context = "\n\n".join(results["documents"][0])

        prompt = f"""
Context:
{context}

Question:
{query}

Answer using only the context above.
"""

        return self.llm.generate_response(prompt)


if __name__ == "__main__":

    rag = RAGPipeline()

    response = rag.analyze(
        "How does a brute force attack work?"
    )

    print(response)