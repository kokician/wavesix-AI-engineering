import os
from llama_index.embeddings.openai import OpenAIEmbedding

def get_embed_model():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY in environment.")
    return OpenAIEmbedding()
