from app.ai.embeddings.embedding_model import EmbeddingModel
from app.ai.rag.vector_store import VectorStore


class Retriever:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.vector_db = VectorStore()

    def retrieve(self, query: str, top_k: int = 3):
        embedding = self.embedder.create_embedding(query)

        results = self.vector_db.search(
            query_embedding=embedding,
            top_k=top_k
        )

        return results


if __name__ == "__main__":

    retriever = Retriever()

    query = "Multiple failed login attempts detected from the same IP address."

    results = retriever.retrieve(query)

    print("\nRetrieved Documents:\n")

    for document in results["documents"][0]:
        print(document)
        print("-" * 60)