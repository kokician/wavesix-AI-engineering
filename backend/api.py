from fastapi import APIRouter, UploadFile, HTTPException, File, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import uuid
import shutil
import os

from rag.document_processor import process_document
from rag.vector_store import get_vector_store, add_documents, delete_document, search_documents, list_all_documents
from rag.llm import generate_response

router = APIRouter()

# In-memory task tracking
processing_tasks = {}

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class Source(BaseModel):
    document_name: str
    page_number: Optional[int] = None
    text: str
    score: float

class QueryResponse(BaseModel):
    response: str
    sources: List[Source] = []

@router.get("/")
async def root():
    return {"message": "RAG Assistant API is running"}

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.post("/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    doc_id = str(uuid.uuid4())
    upload_dir = "data/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{doc_id}.pdf")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    background_tasks.add_task(
        process_and_index_document,
        doc_id=doc_id,
        file_path=file_path,
        file_name=file.filename
    )
    
    return {"id": doc_id, "name": file.filename, "status": "processing"}

async def process_and_index_document(doc_id: str, file_path: str, file_name: str):
    try:
        documents, num_pages = await process_document(file_path, doc_id, file_name)
        add_documents(documents)
        processing_tasks[doc_id] = {
            "status": "completed",
            "name": file_name,
            "pages": num_pages
        }
        print(f"Document {file_name} processed: {len(documents)} chunks created")
    except Exception as e:
        processing_tasks[doc_id] = {"status": "failed", "error": str(e)}
        print(f"Error processing {file_name}: {str(e)}")

@router.get("/documents/{doc_id}")
async def get_document_status(doc_id: str):
    # First check in-memory task cache
    if doc_id in processing_tasks:
        return processing_tasks[doc_id]
    
    # Check vector store
    docs = list_all_documents()
    doc_ids = [doc.metadata.get("doc_id") for doc in docs]
    
    if doc_id in doc_ids:
        return {"status": "completed", "id": doc_id}
    
    # Not found anywhere
    raise HTTPException(status_code=404, detail="Document not found")

@router.delete("/documents/{doc_id}")
async def delete_document_endpoint(doc_id: str):
    try:
        delete_document(doc_id)
        file_path = f"data/uploads/{doc_id}.pdf"
        if os.path.exists(file_path):
            os.remove(file_path)
        processing_tasks.pop(doc_id, None)
        return {"status": "success", "message": "Document deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")

from rag.vector_store import list_all_documents

@router.get("/documents")
async def list_documents():
    docs = list_all_documents()

    doc_map = {}
    for doc in docs:
        doc_id = doc.metadata.get("doc_id")
        if doc_id and doc_id not in doc_map:
            doc_map[doc_id] = {
                "id": doc_id,
                "name": doc.metadata.get("file_name", "Unknown"),
                "pages": doc.metadata.get("total_pages", 0),
            }

    return list(doc_map.values())


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    try:
        results = search_documents(request.query, request.top_k)
        if not results:
            return QueryResponse(
                response="No relevant information found. Try another query or upload more documents.",
                sources=[]
            )
        
        response = await generate_response(request.query, results)
        sources = [
            Source(
                document_name=doc.metadata.get("file_name", "Unknown Document"),
                page_number=doc.metadata.get("page_number"),
                text=doc.get_content(),
                score=score
            )
            for doc, score in results
        ]
        
        return QueryResponse(response=response, sources=sources)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query error: {str(e)}")
