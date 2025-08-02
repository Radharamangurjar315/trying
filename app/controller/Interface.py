from fastapi import APIRouter, HTTPException, Header
from app.models.request_model import EmbedRequest
from app.services.embedder import embedder_instance
from pydantic import BaseModel
from app.services.GetAnswer import process_api_results
from app.settings import settings
ticket = settings.Token

from typing import List
import requests
router = APIRouter()

class interface(BaseModel):
    document_url:str
    queries: List[str]

class interfaceResponse(BaseModel):
    answers: List  # Each dict will have {query, chunks}
    
@router.post("/v1/hackrx/run",response_model=interfaceResponse)
def main(req: interface,authorization: str = Header(None)):

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = authorization.split(" ")[1]

    if token != ticket:
        raise HTTPException(status_code=403, detail="Invalid token")
    else:
        print("Token is valid")
    
    payload = { "document_url": req.document_url}

    response = requests.post("http://localhost:3000/api/extract-info", json=payload)  #For chunking

    data = response.json()

    chunk_list = data["chunk_list"]  # Chunk list created from document's raw text
    
    payload1 = {"texts":chunk_list}

    requests.post("http://localhost:3000/api/embed", json=payload1) #chunklist is embedded and saved to pinecone

    queries = req.queries
 
    payload2 = {"queries":queries}

    response1 = requests.post("http://localhost:3000/api/query",json=payload2)
    
    finalres = process_api_results(response1.json())
    
    return {"status": "ok", "message": "Successful Opr","answers":finalres}




    



    

    