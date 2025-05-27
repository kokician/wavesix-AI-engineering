from dotenv import load_dotenv
import os

from ingestion.loader import load_documents
from ingestion.splitter import split_documents
from ingestion.embedder import get_embed_model
from ingestion.indexer import build_index
from retrieval.query_engine import query_index

def main():
    load_dotenv()
    data_path = os.getenv("SOURCE_DATA", "data")
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"The data path '{data_path}' does not exist.")

    documents = load_documents(data_path)
    nodes = split_documents(documents)
    embed_model = get_embed_model()
    index = build_index(nodes, embed_model)

    while True:
        question = input("\n Your question: ").strip()
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        response = query_index(index, question)
        print("\n Answer:", response)

if __name__ == "__main__":
    main()
