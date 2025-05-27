from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter

def split_documents(documents):
    pipeline = IngestionPipeline(transformations=[TokenTextSplitter()])
    return pipeline.run(documents=documents)
