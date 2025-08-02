from fastapi import FastAPI
from app.settings import settings
from app.routes.extract import router as extract_router
from app.routes.embed import router as embed_router
from app.routes.query_embed import router as query_router
from app.controller.Interface import router as interface_router
app = FastAPI(title="Custom Embedder API")
port = settings.port

@app.get("/emb-status")
async def get_status():
    return {"status": "ok", "message": f"Server is live! at {port}"}

app.include_router(extract_router, prefix="/api")
app.include_router(embed_router, prefix="/api")
app.include_router(query_router, prefix="/api")
app.include_router(interface_router, prefix="/api")
