def build_prompt(goal: str) -> str:
    return f"""
You are an AI engineer assistant. Your job is to help find useful GitHub tools to solve a user's programming or technical goal.

Goal: {goal}

Reason about the task, and if necessary, search GitHub for relevant repos. Then choose one and summarize how to use it.
"""
