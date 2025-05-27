from fastapi import FastAPI, Query
from pydantic import BaseModel
from ingestion.loader import load_documents
from ingestion.splitter import split_documents
from ingestion.embedder import get_embed_model
from ingestion.indexer import build_index
from retrieval.query_engine import query_index

app = FastAPI(title="GitAgent RAG API")

documents = load_documents("data")
nodes = split_documents(documents)
embed_model = get_embed_model()
index = build_index(nodes, embed_model)

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def query_docs(req: QueryRequest):
    response = query_index(index, req.question)
    return {"response": str(response)}
