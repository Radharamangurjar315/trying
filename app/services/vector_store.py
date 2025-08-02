from app.settings import settings
from pinecone import Pinecone
from pinecone import ServerlessSpec
PINECONE_API_KEY = settings.PINECONE_API_KEY
PINECONE_ENVIRONMENT = settings.PINECONE_ENVIRONMENT
INDEX_NAME = settings.PINECONE_INDEX_NAME

pinecone = Pinecone(PINECONE_API_KEY)

if INDEX_NAME in pinecone.list_indexes().names():
    index = pinecone.Index(INDEX_NAME)
else:
        pinecone.create_index(INDEX_NAME, dimension=384,spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            ))  # dimension 384 for MiniLM
print("Pinecone connected Successfully :",INDEX_NAME)
def upsert_vectors(vectors: list[tuple[str, list[float], dict]]):
    batch_size = 100  # You can tweak this depending on performance
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(batch)
    print(f"{len(vectors)} vectors inserted in batches of {batch_size}")
    return {
        "status": "ok",
        "message": f"{len(vectors)} vectors inserted successfully in batches to index {INDEX_NAME}"
    }

    
