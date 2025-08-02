# In this we extracted raw text from the pdf,docx,email raw text:
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.file_parser import download_file, extract_text
from app.services.chunking import chunk_text as get_chunks
router = APIRouter()

class QueryRequest(BaseModel):
    document_url: str
    # queries: List[str]

class QueryResponse(BaseModel):
    chunk_list: List[str]

@router.post("/extract-info", response_model=QueryResponse)
async def extract_info(request: QueryRequest):
    try:
        file_bytes = download_file(request.document_url)
        raw_text = extract_text(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File processing error: {str(e)}")
    
    answers = raw_text
    chunk_list = get_chunks(answers)
    return {"chunk_list": chunk_list}
