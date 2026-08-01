from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import document, search
from dotenv import load_dotenv

# Load environment variables (like GOOGLE_API_KEY) from the .env file
load_dotenv()

app = FastAPI(
    title="FinSight AI API",
    description="Backend API for the FinSight Financial Document Analysis Platform",
    version="1.0.0"
)

# Allow our React frontend (running on port 5173) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document.router, prefix="/api")
app.include_router(search.router, prefix="/api")

@app.get("/")
async def root():
    """
    Health check endpoint to verify the API is running.
    """
    return {"message": "Welcome to the FinSight AI API", "status": "running"}
