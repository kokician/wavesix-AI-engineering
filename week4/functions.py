from tools.github_search import search_github_repos
from tools.repo_analyzer import analyze_repo

function_specs = [
    {
        "type": "function",
        "function": {
            "name": "search_github",
            "description": "Search for GitHub repositories based on a user goal",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_repo",
            "description": "Summarize a GitHub repository and extract install/run instructions",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string"}
                },
                "required": ["repo_url"]
            }
        }
    }
]

functions_map = {
    "search_github": lambda query: search_github_repos(query),
    "summarize_repo": lambda repo_url: analyze_repo(repo_url)
}
