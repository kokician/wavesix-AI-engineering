from typing import List, Tuple
from pypdf import PdfReader
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding

async def process_document(file_path: str, doc_id: str, file_name: str) -> Tuple[List[Document], int]:
    """
    Process a PDF document, extract text, and chunk it.
    Returns a list of Document objects and the number of pages.
    """
    try:
        # Read PDF
        reader = PdfReader(file_path)
        num_pages = len(reader.pages)
        
        # Extract text from each page
        documents = []
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if not text.strip():
                continue
                
            # Create a document with metadata
            doc = Document(
                text=text,
                metadata={
                    "doc_id": doc_id,
                    "file_name": file_name,
                    "page_number": i + 1,
                    "total_pages": num_pages
                }
            )
            documents.append(doc)
        
        # Create a sentence splitter for chunking
        splitter = SentenceSplitter(
            chunk_size=1024,
            chunk_overlap=200,
            paragraph_separator="\n\n",
            secondary_chunking_regex="[^.!?]*[.!?]",
        )
        
        # Split documents into chunks
        chunked_documents = []
        for doc in documents:
            # Split the document but preserve metadata
            nodes = splitter.get_nodes_from_documents([doc])
            
            # Convert nodes back to Documents with original metadata
            for i, node in enumerate(nodes):
                chunk_doc = Document(
                    text=node.text,
                    metadata={
                        **doc.metadata,
                        "chunk_id": i,
                    }
                )
                chunked_documents.append(chunk_doc)
        
        embed_model = OpenAIEmbedding()
        vectors = [embed_model.get_text_embedding(doc.text) for doc in chunked_documents]

        return chunked_documents, num_pages, vectors
        
    except Exception as e:
        print(f"Error processing document: {str(e)}")
        raise e