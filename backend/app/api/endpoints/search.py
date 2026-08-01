from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.vector_service import vector_db
from app.services.llm_service import llm

router = APIRouter(
    prefix="/search",
    tags=["search"]
)

class SearchQuery(BaseModel):
    query: str
    top_k: int = 3

@router.post("/")
async def semantic_search(search_req: SearchQuery):
    """
    Accepts a search query, retrieves relevant chunks from Qdrant, 
    and uses Google Gemini to generate a conversational answer.
    """
    if not search_req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
        
    try:
        # 1. Retrieve the raw chunks from Qdrant
        raw_results = vector_db.search(query=search_req.query, top_k=search_req.top_k)
        
        # 2. Pass the question and the chunks to Gemini
        ai_answer = llm.answer_question(query=search_req.query, context_chunks=raw_results)
            
        return {
            "query": search_req.query,
            "answer": ai_answer,
            "citations": raw_results  # We return the chunks so the frontend can show sources!
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
