import requests
import json
from agents import RepoAnalyzer, CriticAgent, FixerAgent, IssueAgent
from dotenv import load_dotenv

load_dotenv()

repo_analyzer = RepoAnalyzer("RepoAnalyzer")
critic_agent = CriticAgent("CriticAgent")
fixer_agent = FixerAgent("FixerAgent")
issue_agent = IssueAgent("IssueAgent")

GITHUB_SEARCH_API = "https://api.github.com/search/repositories"

def search_top_repos(query, top_n=3):
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": top_n
    }
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(GITHUB_SEARCH_API, params=params, headers=headers)
    if response.status_code != 200:
        raise Exception(f"GitHub search failed: {response.text}")
    items = response.json().get("items", [])
    return [item["html_url"] for item in items]

def main():
    user_query = input("Enter a topic to search GitHub repos (e.g. 'data visualization'): ")
    repo_urls = search_top_repos(user_query)

    for idx, repo_url in enumerate(repo_urls, 1):
        print(f"\n--- Processing Repo #{idx}: {repo_url} ---")

        analysis = repo_analyzer.analyze(repo_url)
        if isinstance(analysis, str):
            print(f"Analysis failed: {analysis}")
            continue

        issues = critic_agent.critique(repo_url, analysis)
        print("Critique:", issues)

        suggestions = fixer_agent.debate(repo_url, issues)
        print("Suggestions:", suggestions)

        formatted_issues = issue_agent.create_issues(analysis['repo'], issues, suggestions)
        created = issue_agent.open_github_issues(formatted_issues)
        print("Issue creation results:", created)

if __name__ == "__main__":
    main()
