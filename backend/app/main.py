from fastapi import FastAPI
from app.api.endpoints import document, search
from dotenv import load_dotenv

# Load environment variables (like GOOGLE_API_KEY) from the .env file
load_dotenv()

app = FastAPI(
    title="FinSight AI API",
    description="Backend API for the FinSight Financial Document Analysis Platform",
    version="1.0.0"
)

app.include_router(document.router, prefix="/api")
app.include_router(search.router, prefix="/api")

@app.get("/")
async def root():
    """
    Health check endpoint to verify the API is running.
    """
    return {"message": "Welcome to the FinSight AI API", "status": "running"}
