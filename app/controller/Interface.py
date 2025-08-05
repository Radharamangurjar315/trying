from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import List, Any
import requests

from app.services.GetAnswer import process_api_results
from app.settings import settings

router = APIRouter()
ticket = settings.Token

class interface(BaseModel):
    document_url: str
    queries: List[str]

class AnswerItem(BaseModel):
    question: str
    answer: str

class interfaceResponse(BaseModel):
    status: str
    message: str
    answers: List[AnswerItem]


@router.post("/v1/hackrx/run", response_model=interfaceResponse)
def main(req: interface, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.split(" ")[1]
    if token != ticket:
        raise HTTPException(status_code=403, detail="Invalid token")

    # Step 1: Chunking
    try:
        response = requests.post("http://localhost:3000/api/extract-info", json={"document_url": req.document_url})
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"extract-info failed: {str(e)}")
    except ValueError:
        raise HTTPException(status_code=500, detail=f"extract-info returned invalid JSON: {response.text}")

    chunk_list = data.get("chunk_list")
    if not chunk_list:
        raise HTTPException(status_code=500, detail="No chunks found in extract-info response")

    # Step 2: Embedding
    try:
        embed_response = requests.post("http://localhost:3000/api/embed", json={"texts": chunk_list})
        embed_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"embed failed: {str(e)}")

    # Step 3: Querying
    try:
        response1 = requests.post("http://localhost:3000/api/query", json={"queries": req.queries})
        response1.raise_for_status()
        result_data = response1.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"query failed: {str(e)}")
    except ValueError:
        raise HTTPException(status_code=500, detail=f"query returned invalid JSON: {response1.text}")

    # Step 4: Process Results
    answers = process_api_results(result_data)  # assumed to be a list of answers

    # Pair questions with answers
    paired_qa = [{"question": q, "answer": a} for q, a in zip(req.queries, answers)]

    return {
        "status": "ok",
        "message": "Successful Operation",
        "answers": paired_qa
    }
