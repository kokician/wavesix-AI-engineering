import os
from dotenv import load_dotenv
load_dotenv()  

from openai import OpenAI
import chromadb

EMBEDDING_MODEL = "text-embedding-ada-002"
DATA_FILE = os.getenv("DATA_FILE", "data/knowledge.txt")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Persistent Chroma client
chroma_client = chromadb.PersistentClient(path="data/chroma")
collection = chroma_client.get_or_create_collection("docs")

def embed_text(texts):

    clean_texts = [text for text in texts if isinstance(text, str) and text.strip()]
    if not clean_texts:
        raise ValueError("No valid texts to embed.")

    response = client.embeddings.create(input=clean_texts, model=EMBEDDING_MODEL)
    return [item.embedding for item in response.data]

def load_docs():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


if len(collection.get()["ids"]) == 0:
    docs = load_docs()
    embeddings = embed_text(docs)
    collection.add(documents=docs, embeddings=embeddings, ids=[str(i) for i in range(len(docs))])

def get_similar_docs(query, top_k=3):
    query_embedding = embed_text([query])[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return "\n".join(results["documents"][0])
