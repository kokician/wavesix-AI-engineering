from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent

app = FastAPI(title="GitAgent-lite API")

class ToolRequest(BaseModel):
    goal: str

@app.post("/suggest-tool")
def suggest_tool(request: ToolRequest):
    result = run_agent(request.goal)
    return {"goal": request.goal, "suggested_tool": result}
