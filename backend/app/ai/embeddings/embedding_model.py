from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(self):
        """
        Load the embedding model only once.
        """
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def create_embedding(self, text: str):
        """
        Convert text into a vector embedding.
        """
        return self.model.encode(text).tolist()


# Test the model
if __name__ == "__main__":
    embedding = EmbeddingModel()

    sample = """
    Failed login attempt detected from IP 192.168.1.15.
    Multiple authentication failures observed.
    """

    vector = embedding.create_embedding(sample)

    print(f"Embedding Length: {len(vector)}")
    print(vector[:10])  # Print first 10 values