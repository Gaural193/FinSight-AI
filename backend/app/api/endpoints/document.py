from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_service import document_processor
from app.services.vector_service import vector_db

router = APIRouter(
    prefix="/upload",
    tags=["documents"]
)

@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    """
    Accepts a PDF file upload, extracts the text, splits it into chunks,
    and stores the chunks as vector embeddings in Qdrant.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        # 1. Read the raw file bytes into memory
        file_bytes = await file.read()
        
        # 2. Extract and chunk the text
        chunks = document_processor.process_pdf_bytes(file_bytes)
        
        if not chunks:
            return {"message": "No text could be extracted. The PDF might be empty or scanned."}
            
        # 3. Store the chunks in the Vector Database (Qdrant)
        stored_count = vector_db.store_chunks(chunks=chunks, filename=file.filename)
            
        return {
            "message": "Success! PDF processed and indexed into Vector Database.",
            "filename": file.filename,
            "total_chunks_created": len(chunks),
            "total_vectors_stored": stored_count
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
