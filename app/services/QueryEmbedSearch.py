from app.services.vector_store import index  # pinecone.Index instance
from app.services.embedder import embedder_instance
from datetime import datetime
def query_pinecone(query_text: str, top_k=5):
    # Embed user query
    query_embedding = embedder_instance.model.encode([query_text], normalize_embeddings=True)[0].tolist()
    # Query Pinecone
    results = index.query(
    namespace="__default__",
    vector=query_embedding, 
    top_k=5,
    include_metadata=True,
    include_values=False
)
    # Extract matched chunks
    matched_chunks = [match['metadata']['text'] for match in results['matches']]
    return matched_chunks