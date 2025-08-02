# from sentence_transformers import SentenceTransformer
# from app.config import MODEL_NAME, DEVICE

# class Embedder:
#     def __init__(self):
#         self.model = SentenceTransformer(MODEL_NAME)
#         self.model.to(DEVICE)

#     def get_embeddings(self, texts: list[str]) -> list[list[float]]:
#         return self.model.encode(texts, normalize_embeddings=True).tolist()

# embedder_instance = Embedder()

from app.services.vector_store import upsert_vectors
from sentence_transformers import SentenceTransformer
from app.config import MODEL_NAME, DEVICE
import uuid

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.model.to(DEVICE)

    def get_embeddings(self, texts: list[str]) -> list[tuple[str, list[float], dict]]:
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        vectors = []
        for text, embed in zip(texts, embeddings):
            id = str(uuid.uuid4())
            metadata = {"text": text}
            vectors.append((id, embed.tolist(), metadata))
        # Upsert to Pinecone
        upsert_vectors(vectors)
        return vectors  # return vector info if needed
embedder_instance = Embedder()
