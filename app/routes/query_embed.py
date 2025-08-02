from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.QueryEmbedSearch import query_pinecone
router = APIRouter()

class QueryRequest(BaseModel):
    queries: List[str]  # Change from 'query' to 'queries'

class QueryResponse(BaseModel):
    results: List[dict]  # Each dict will have {query, chunks}

@router.post("/query", response_model=QueryResponse)
def answer_query(req: QueryRequest):
    results = []

    for query in req.queries:
        chunks = query_pinecone(query)
        results.append({"query": query, "chunks": chunks})
        

    return {"status": "ok", "message": f"Server is live! at","results":results}