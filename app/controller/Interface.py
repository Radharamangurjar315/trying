from fastapi import APIRouter
from app.models.request_model import EmbedRequest
from app.services.embedder import embedder_instance
from pydantic import BaseModel
from app.services.GetAnswer import process_api_results
from app.services.vector_store import generate_namespace_from_url, namespace_exists, upsert_vectors
from typing import List
import requests
router = APIRouter()

class interface(BaseModel):
    documents:str
    questions: List[str]

class interfaceResponse(BaseModel):
    answers: List  # Each dict will have {query, chunks}
    
@router.post("/v1/hackrx/run",response_model=interfaceResponse)

def main(req: interface):

    namespace = generate_namespace_from_url(req.documents)

    if namespace_exists(namespace):

        queries = req.questions
 
        payload2 = {"queries":queries,"namespace":namespace}

        response1 = requests.post("http://localhost:3000/api/query",json=payload2)
    
        finalres = process_api_results(response1.json())
    
        return {"status": "ok", "message": "Successful Opr","answers":finalres}
    else:
        namespace = generate_namespace_from_url(req.documents)
        payload = { "document_url": req.documents}
    
        response = requests.post("http://localhost:3000/api/extract-info", json=payload)  #For chunking

        data = response.json()

        chunk_list = data["chunk_list"]  # Chunk list created from document's raw text
    
        payload1 = {"texts":chunk_list,"namespace":namespace}

        emb_res = requests.post("http://localhost:3000/api/embed", json=payload1).json() #chunklist is embedded and saved to pinecone
        if emb_res.get("status")=='ok':
            import time
            time.sleep(5)
            queries = req.questions
 
            payload2 = {"queries":queries,"namespace":namespace}

            response1 = requests.post("http://localhost:3000/api/query",json=payload2)
    
            finalres = process_api_results(response1.json())
    
            return {"status": "ok", "message": "Successful Opr","answers":finalres}
        else:
            print("❌ Embedding failed. Stopping process.")
            return {"status": "error", "message": "Embedding failed", "answers": []}