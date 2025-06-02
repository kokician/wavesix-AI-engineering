import os
from langchain_openai import OpenAIEmbeddings  # updated import
from langchain_community.vectorstores import Chroma
from langchain.memory import VectorStoreRetrieverMemory
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI  # updated import

PERSIST_DIR = "chroma_db"

def get_memory():
    os.makedirs(PERSIST_DIR, exist_ok=True)
    embedding = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embedding)
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    memory = VectorStoreRetrieverMemory(retriever=retriever)
    return memory

def save_context(memory, input_text: str, output_text: str):
    doc = Document(page_content=f"Input: {input_text}\nOutput: {output_text}")
    # Access vectorstore through retriever
    memory.retriever.vectorstore.add_documents([doc])
    memory.retriever.vectorstore.persist()

def get_memory_qa_chain():
    os.makedirs(PERSIST_DIR, exist_ok=True)
    embedding = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embedding)
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True
    )
    return qa_chain
