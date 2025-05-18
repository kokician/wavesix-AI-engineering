import os
from typing import List, Tuple
from llama_index.core import Document
from llama_index.llms.openai import OpenAI
from llama_index.core.settings import Settings
import asyncio

def configure_llm():
    api_key = os.environ.get("OPENAI_API_KEY")
    llm = OpenAI(model="gpt-4.1", api_key=api_key)
    Settings.llm = llm

configure_llm()

async def generate_response(query: str, context: List[Tuple[Document, float]]) -> str:
    """Generate a response using the LLM with context from retrieved documents"""
    if not context:
        return "I couldn't find any relevant information to answer your question."
    
    sorted_context = sorted(context, key=lambda x: x[1], reverse=True)

    context_texts = [
        f"Document: {doc.metadata.get('file_name', 'Unknown')}, Page: {doc.metadata.get('page_number', 'Unknown')}\n{doc.get_content()}\n\n"
        for doc, _ in sorted_context
    ]

    prompt = f"""You are a helpful assistant that answers questions based on the provided document context.
Answer the question based ONLY on the context provided below. If the information isn't in the context, say you don't have enough information to answer.
Use precise references to support your answer. Be clear, concise, and helpful.

CONTEXT:
{' '.join(context_texts)}

QUESTION: {query}

ANSWER:"""

    response = await Settings.llm.acomplete(prompt)
    return response.text


async def summarize_passage(passage: str, query: str = "") -> str:
    """Summarize a passage using the LLM, optionally conditioned on a query."""
    if query:
        prompt = f"You are helping answer the question: '{query}'.\nSummarize the following passage to help answer it:\n\n{passage}"
    else:
        prompt = f"Summarize the following passage in 2-3 sentences:\n\n{passage}"

    response = await Settings.llm.acomplete(prompt)
    return response.text.strip()
