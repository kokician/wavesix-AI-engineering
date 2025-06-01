import chromadb
import os
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.PersistentClient(path="chroma_store")
collection = chroma_client.get_or_create_collection(name="github_memory_v2")

def embed(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

def save_to_vector_memory(user_input, summary):
    embedding = embed(user_input)
    collection.add(documents=[summary], embeddings=[embedding], ids=[user_input])

def search_vector_memory(user_input):
    embedding = embed(user_input)
    results = collection.query(query_embeddings=[embedding], n_results=1)
    docs = results.get("documents", [])
    if docs and docs[0]:
        return docs[0][0]
    return None

def save_chat_memory(repo_url, message):
    embedding = embed(repo_url + "_chat")
    collection.add(
        documents=[message],
        embeddings=[embedding],
        ids=[repo_url + "_chat"]
    )

def get_chat_memory(repo_url):
    embedding = embed(repo_url + "_chat")
    results = collection.query(query_embeddings=[embedding], n_results=1)
    docs = results.get("documents", [])
    if docs and docs[0]:
        return docs[0][0]
    return ""

def clear_memory(repo_url):
    try:
        collection.delete(ids=[repo_url + "_chat"])
    except Exception as e:
        print("Memory deletion failed:", e)
