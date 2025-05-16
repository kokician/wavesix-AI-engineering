from typing import List, Tuple
from llama_index.core import Document
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex, StorageContext
import chromadb
import os

# Initialize global variables
_chroma_client = None
_chroma_collection = None
_vector_store = None
_index = None

def get_chroma_client():
    """Get or create ChromaDB client"""
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(path="./data/indexes")
    return _chroma_client

def get_chroma_collection():
    """Get or create ChromaDB collection"""
    global _chroma_collection
    if _chroma_collection is None:
        client = get_chroma_client()
        # Get collection or create if it doesn't exist
        _chroma_collection = client.get_or_create_collection("rag_documents")
    return _chroma_collection

def get_vector_store():
    """Get or create vector store"""
    global _vector_store
    if _vector_store is None:
        collection = get_chroma_collection()
        _vector_store = ChromaVectorStore(chroma_collection=collection)
    return _vector_store

def get_index():
    """Get or create vector index"""
    global _index
    if _index is None:
        vector_store = get_vector_store()
        
        # Get API key and validate it
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY is not set in the environment variables.")

        embed_model = OpenAIEmbedding(
            model="text-embedding-3-small", 
            api_key=api_key
        )
        
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        _index = VectorStoreIndex.from_vector_store(
            vector_store,
            storage_context=storage_context,
            embed_model=embed_model,
        )
    return _index


def add_documents(documents: List[Document]):
    """Add documents to the vector store"""
    if not documents:
        return
        
    index = get_index()
    index.insert_nodes(documents)
    
def delete_document(doc_id: str):
    """Delete all chunks for a document by doc_id"""
    vector_store = get_vector_store()
    index = get_index()
    
    # Get all nodes
    all_nodes = vector_store.get()
    
    # Find nodes matching the doc_id
    nodes_to_delete = []
    for node in all_nodes:
        if node.metadata.get("doc_id") == doc_id:
            nodes_to_delete.append(node.id_)
            
    # Delete nodes if any found
    if nodes_to_delete:
        vector_store.delete(nodes_to_delete)

def search_documents(query: str, top_k: int = 5) -> List[Tuple[Document, float]]:
    """Search for documents matching the query"""
    if not query:
        return []
        
    index = get_index()
    retriever = index.as_retriever(similarity_top_k=top_k)
    results = retriever.retrieve(query)
    
    # Convert to (Document, score) tuples
    return [(node.node, node.score) for node in results]

def list_all_documents() -> List[Document]:
    """Return all documents from the vector store."""
    vector_store = get_vector_store()
    index = get_index()
    nodes = index.vector_store._collection.get(include=["metadatas", "documents"])
    
    documents = []
    for metadata, document in zip(nodes["metadatas"], nodes["documents"]):
        doc = Document(text=document, metadata=metadata)
        documents.append(doc)
    return documents

def document_exists(doc_id: str) -> bool:
    vector_store = get_vector_store()
    index = get_index()
    nodes = index.vector_store._collection.get(
        where={"doc_id": doc_id},
        include=["metadatas"]
    )
    return len(nodes["metadatas"]) > 0
