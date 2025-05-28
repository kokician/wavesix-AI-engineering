from dotenv import load_dotenv
import os
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from ingestion.loader import load_documents
from ingestion.splitter import split_documents
from ingestion.embedder import get_embed_model
from ingestion.indexer import build_index
from retrieval.query_engine import query_index
from retrieval.pure_prompt import pure_prompt

from llama_index.core.indices.keyword_table import SimpleKeywordTableIndex
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.retrievers import VectorIndexRetriever


# Setup retrievers
def setup_retrievers(index, documents):
    bm25_retriever = BM25Retriever(documents) 
    vector_retriever = VectorIndexRetriever(index)
    return bm25_retriever, vector_retriever

# Combine results 
def hybrid_retrieve(bm25, vector, query):
    bm25_results = bm25.retrieve(query)
    vector_results = vector.retrieve(query)

    all_nodes = {node.node_id: node for node in bm25_results + vector_results}
    combined = list(all_nodes.values())[:5] 
    return combined

# File Watcher for auto-rebuild 
class RebuildHandler(FileSystemEventHandler):
    def __init__(self, data_path, rebuild_callback):
        self.data_path = data_path
        self.rebuild_callback = rebuild_callback

    def on_modified(self, event):
        if event.src_path.endswith(".txt") or event.is_directory:
            print("\nChange detected. Rebuilding index...")
            self.rebuild_callback()

def start_watcher(data_path, rebuild_callback):
    observer = Observer()
    handler = RebuildHandler(data_path, rebuild_callback)
    observer.schedule(handler, path=data_path, recursive=True)
    observer_thread = Thread(target=observer.start)
    observer_thread.daemon = True
    observer_thread.start()

# Rebuild index on data change 
def rebuild_index(data_path):
    documents = load_documents(data_path)
    nodes = split_documents(documents)
    embed_model = get_embed_model()
    index = build_index(nodes, embed_model)
    bm25, vector = setup_retrievers(index, documents)
    return index, bm25, vector, documents

def main():
    load_dotenv()
    data_path = os.getenv("SOURCE_DATA", "data")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"The data path '{data_path}' does not exist.")

    index, bm25_retriever, vector_retriever, documents = rebuild_index(data_path)
    search_mode = "vector"

    start_watcher(data_path, lambda: rebuild_index(data_path))

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
            if search_mode == "hybrid":
                results = hybrid_retrieve(bm25_retriever, vector_retriever, question)
                print("\nSources:")
                for node in results:
                    print(f"- {node.metadata.get('file_path', 'unknown source')}")
                print("\nAnswer:", "\n".join([n.text for n in results]))
            else:
                response = query_index(index, question, mode="vector")
                print("\nAnswer:", response)

if __name__ == "__main__":
    main()
