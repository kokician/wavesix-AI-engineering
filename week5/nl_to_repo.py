import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_repo_url_from_nl(natural_language_query: str) -> str:
    prompt = (
        f"You are a helpful assistant. "
        f"Given the user query, respond ONLY with the most relevant GitHub repository URL for a Python project.\n"
        f"Query: \"{natural_language_query}\"\n"
        f"Response:"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        repo_url = response.choices[0].message.content.strip()
        
        if repo_url.startswith("https://github.com") or repo_url.startswith("http://github.com"):
            return repo_url
        else:
            return None
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None