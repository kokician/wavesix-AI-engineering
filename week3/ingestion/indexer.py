import os
from chromadb import Client
from chromadb.config import Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage

def build_index(nodes=None, embed_model=None):
    persist_dir = "./chroma_storage"
    collection_name = "docs"
    docstore_path = os.path.join(persist_dir, "docstore.json")

    chroma_client = Client(Settings(persist_directory=persist_dir))

    if collection_name in [c.name for c in chroma_client.list_collections()]:
        collection = chroma_client.get_collection(collection_name)
    else:
        collection = chroma_client.create_collection(collection_name)

    vector_store = ChromaVectorStore(chroma_collection=collection)

    if os.path.exists(docstore_path):
        storage_context = StorageContext.from_defaults(
            persist_dir=persist_dir,
            vector_store=vector_store
        )
        index = load_index_from_storage(storage_context)
    else:
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store
        )
        index = VectorStoreIndex(nodes, storage_context=storage_context)
        index.storage_context.persist() 

    return index
