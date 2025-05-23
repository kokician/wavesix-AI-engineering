from typing import List, Tuple
from pypdf import PdfReader
from llama_index.core import Document
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding


async def process_document(file_path: str, doc_id: str, file_name: str) -> Tuple[List[Document], int, List[List[float]]]:
    """
    Process a PDF document, extract text, and semantically chunk it.
    Returns a list of Document objects, number of pages, and their semantic vectors.
    """
    try:
        reader = PdfReader(file_path)
        num_pages = len(reader.pages)

        documents = []

        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if not text or not text.strip():
                continue

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

        embed_model = OpenAIEmbedding(model="text-embedding-3-small")

        splitter = SemanticSplitterNodeParser(
            embed_model=embed_model,
            chunk_size=1024,
            chunk_overlap=200,
        )

        chunked_documents = []
        vectors = []

        for doc in documents:
            nodes = splitter.get_nodes_from_documents([doc])
            for i, node in enumerate(nodes):
                chunk_doc = Document(
                    text=node.text,
                    metadata={
                        **doc.metadata,
                        "chunk_id": i,
                    }
                )
                chunked_documents.append(chunk_doc)

                vector = embed_model.get_text_embedding(node.text)
                vectors.append(vector)

        return chunked_documents, num_pages, vectors

    except Exception as e:
        print(f"Error processing document: {str(e)}")
        raise e
