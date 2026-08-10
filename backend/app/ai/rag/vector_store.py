import chromadb
from chromadb.config import Settings


class VectorStore:
    def __init__(self):
        # Create local ChromaDB database
        self.client = chromadb.PersistentClient(path="chroma_db")

        # Create/Get collection
        self.collection = self.client.get_or_create_collection(
            name="cybersecurity_knowledge"
        )

    def add_document(self, doc_id: str, text: str, embedding: list):
        """
        Store a document and its embedding.
        """
        self.collection.add(
            ids=[doc_id],
            documents=[text],
            embeddings=[embedding]
        )

    def search(self, query_embedding: list, top_k: int = 3):
        """
        Search similar documents.
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results


# ---------------- TEST ---------------- #

if __name__ == "__main__":
    from app.ai.embeddings.embedding_model import EmbeddingModel

    embedder = EmbeddingModel()
    vector_db = VectorStore()

    sample_text = "Brute force attack detected from multiple failed login attempts."

    embedding = embedder.create_embedding(sample_text)

    vector_db.add_document(
        doc_id="doc1",
        text=sample_text,
        embedding=embedding
    )

    result = vector_db.search(embedding)

    print("\nSearch Results:")
    print(result)