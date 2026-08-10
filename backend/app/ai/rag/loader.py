import os

from app.ai.embeddings.embedding_model import EmbeddingModel
from app.ai.rag.vector_store import VectorStore


class KnowledgeLoader:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.vector_db = VectorStore()

    def load_documents(self, folder_path):
        supported_extensions = [".txt"]

        count = 0

        for filename in os.listdir(folder_path):

            if not any(filename.endswith(ext) for ext in supported_extensions):
                continue

            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            embedding = self.embedder.create_embedding(text)

            self.vector_db.add_document(
                doc_id=filename,
                text=text,
                embedding=embedding
            )

            count += 1
            print(f"Loaded: {filename}")

        print(f"\nSuccessfully loaded {count} documents.")


if __name__ == "__main__":

    loader = KnowledgeLoader()

    loader.load_documents("knowledge_base")