import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="chroma_store")
collection = client.get_or_create_collection(name="github_memory")

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text):
    return embedder.encode([text])[0].tolist()

def save_to_vector_memory(user_input, summary):
    embedding = embed(user_input)
    collection.add(documents=[summary], embeddings=[embedding], ids=[user_input])

def search_vector_memory(user_input):
    embedding = embed(user_input)
    results = collection.query(query_embeddings=[embedding], n_results=1)
    return results["documents"][0][0] if results["documents"] else None
