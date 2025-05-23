from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router as api_router
import os

app = FastAPI(title="RAG Assistant API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Ensures Required Data Directories Exist ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
DATA_DIR = os.path.join(BASE_DIR, "data")
REQUIRED_DIRS = ["uploads", "indexes", "vectors"]

for folder in REQUIRED_DIRS:
    os.makedirs(os.path.join(DATA_DIR, folder), exist_ok=True)

# === Include API Router ===
app.include_router(api_router)

# === Run Server ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
