from dotenv import load_dotenv
load_dotenv() 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router as api_router  
import os


app = FastAPI(title="RAG Assistant API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directories exist
os.makedirs("backend/data/uploads", exist_ok=True)
os.makedirs("backend/data/indexes", exist_ok=True)

# Include API routes
app.include_router(api_router)

# Run with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

