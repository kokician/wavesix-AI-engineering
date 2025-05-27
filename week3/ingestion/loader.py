from llama_index.core import SimpleDirectoryReader

def load_documents(data_path: str):
    return SimpleDirectoryReader(data_path).load_data()
