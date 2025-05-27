from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from openai import OpenAI
from prompts import format_prompt
from logger import log_prompt
from vector_store import get_similar_docs

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(payload: Question):
    question = payload.question
    matched_docs = get_similar_docs(question)
    prompt = format_prompt(matched_docs, question)
    log_prompt(prompt)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message.content.strip()
    return {"response": answer}
