from dotenv import load_dotenv
import os

from ingestion.loader import load_documents
from ingestion.splitter import split_documents
from ingestion.embedder import get_embed_model
from ingestion.indexer import build_index
from retrieval.query_engine import query_index
from retrieval.pure_prompt import pure_prompt

def main():
    load_dotenv()
    data_path = os.getenv("SOURCE_DATA", "data")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"The data path '{data_path}' does not exist.")

    documents = load_documents(data_path)
    nodes = split_documents(documents)
    embed_model = get_embed_model()
    index = build_index(nodes, embed_model)

    search_mode = "vector"
    while True:
        question = input(f"\nYour question (mode: {search_mode}) [type 'mode' to toggle, 'pure' for GPT-only, 'exit' to quit]: ").strip()
        if question.lower() == "exit":
            print("Goodbye!")
            break
        elif question.lower() == "pure":
            q = input("Ask GPT directly: ").strip()
            print("\nAnswer:", pure_prompt(q))
        elif question.lower() == "mode":
            search_mode = "hybrid" if search_mode == "vector" else "vector"
            print(f"Switched to {search_mode} search mode.")
        else:
            response = query_index(index, question, mode=search_mode)
            print("\nAnswer:", response)

if __name__ == "__main__":
    main()
