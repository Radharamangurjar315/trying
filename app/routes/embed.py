from fastapi import APIRouter
from app.models.request_model import EmbedRequest
from app.services.embedder import embedder_instance

router = APIRouter()

@router.post("/embed")
def embed_texts(req: EmbedRequest):
    vectors = embedder_instance.get_embeddings(req.texts,req.namespace)
    print("Chunks Are embedded and Saved")
    return {"status": "ok", "message": f"work is done"}