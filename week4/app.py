from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from agents import Runner
from agent.github_agents import github_agent

load_dotenv()

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
async def ask_agent(request: QueryRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="Missing API key")

    try:
        result = await Runner.run(github_agent, request.query)
        return {"response": result.final_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
