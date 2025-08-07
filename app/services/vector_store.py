import hashlib
from app.settings import settings
from pinecone import Pinecone
from pinecone import ServerlessSpec
PINECONE_API_KEY = settings.PINECONE_API_KEY
PINECONE_ENVIRONMENT = settings.PINECONE_ENVIRONMENT
INDEX_NAME = settings.PINECONE_INDEX_NAME

pinecone = Pinecone(PINECONE_API_KEY)

if INDEX_NAME in pinecone.list_indexes().names():
    index = pinecone.Index(INDEX_NAME)
    print("Pinecone connected Successfully :",INDEX_NAME)
else:
        pinecone.create_index(INDEX_NAME, dimension=384,spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            ))  # dimension 384 for MiniLM
        print(f"Pinecone index created is : {INDEX_NAME}")
        print("Pinecone connected Successfully :",INDEX_NAME)
        index = pinecone.Index(INDEX_NAME)
# 🔹 Generate namespace from doc URL (hash + safe prefix)
def generate_namespace_from_url(url: str) -> str:
    return "ns_" + hashlib.sha256(url.encode()).hexdigest()[:16]


# 🔹 Check if namespace already exists (by trying a dummy query)
def namespace_exists(namespace: str) -> bool:
    try:
        res = index.query(
            namespace=namespace,
            vector=[0.0] * 384,  # dummy vector
            top_k=1
        )
        return len(res.get("matches", [])) > 0
    except Exception:
        return False


# 🔹 Insert vectors into Pinecone (in batches)
def upsert_vectors(vectors: list[tuple[str, list[float], dict]], namespace: str):
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch, namespace=namespace)

    print(f"✅ {len(vectors)} vectors inserted into namespace '{namespace}'")
    return {
        "status": "ok",
        "message": f"{len(vectors)} vectors inserted successfully into namespace '{namespace}'"
    }
