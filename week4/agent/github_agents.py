import os
import requests
from dotenv import load_dotenv
from agents import Agent, function_tool
from utils.github_utils import extract_user_repo

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github.v3.raw",
    "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else None
}

@function_tool
def analyze_repo(repo_url: str) -> str:
    """Extract install/usage info from GitHub README."""
    try:
        user_repo = extract_user_repo(repo_url)
        api_url = f"https://api.github.com/repos/{user_repo}/readme"
        res = requests.get(api_url, headers=HEADERS)
        res.raise_for_status()
        readme = res.text
        lines = [l for l in readme.splitlines() if "install" in l.lower() or "$" in l or "usage" in l.lower()]
        return "\n".join(lines[:10]) if lines else "No installation or usage information found."
    except Exception as e:
        return f"Error analyzing repo: {str(e)}"

@function_tool
def search_github_repos(query: str) -> str:
    """Search GitHub for repositories using a query."""
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"
    try:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        repos = res.json().get("items", [])[:3]
        if not repos:
            return "No repositories found."
        return "\n".join([f"{r['name']}: {r['html_url']}" for r in repos])
    except Exception as e:
        return f"Error searching GitHub: {str(e)}"

github_agent = Agent(
    name="GitHub Repository Assistant",
    instructions="""
    You help users search GitHub and analyze repositories. 
    Use 'search_github_repos' for finding repositories, 
    and 'analyze_repo' to extract install or usage info from READMEs.
    """,
    tools=[analyze_repo, search_github_repos]
)
