from fastapi import FastAPI
from app.api.endpoints import document

app = FastAPI(
    title="FinSight AI API",
    description="Backend API for the FinSight Financial Document Analysis Platform",
    version="1.0.0"
)

app.include_router(document.router, prefix="/api")

@app.get("/")
async def root():
    """
    Health check endpoint to verify the API is running.
    """
    return {"message": "Welcome to the FinSight AI API", "status": "running"}
