import os
import json 
import requests
from autogen import ConversableAgent
from dotenv import load_dotenv
from utils.github_utils import extract_user_repo
from memory.vector_memory import save_to_vector_memory, search_vector_memory

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github.v3.raw",
    "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else None
}

class RepoAnalyzer(ConversableAgent):
    def analyze(self, repo_url):
        cached = search_vector_memory(repo_url)
        if cached:
            return json.loads(cached)

        user_repo = extract_user_repo(repo_url)
        readme_res = requests.get(f"https://api.github.com/repos/{user_repo}/readme", headers=HEADERS)
        tree_res = requests.get(f"https://api.github.com/repos/{user_repo}/git/trees/main?recursive=1", headers=HEADERS)
        if readme_res.status_code != 200 or tree_res.status_code != 200:
            return "Error fetching README or repo tree."
        
        readme_text = readme_res.text
        files = [item['path'] for item in tree_res.json().get('tree', []) if item['type'] == 'blob']
        tech_stack = [f for f in files if 'package.json' in f or 'requirements.txt' in f or 'setup.py' in f]
        result = {
            "repo": user_repo,
            "readme": readme_text[:1500],
            "files": files[:100],
            "tech_files": tech_stack
        }
        save_to_vector_memory(repo_url, json.dumps(result))
        return result

class CriticAgent(ConversableAgent):
    def critique(self, analysis):
        readme = analysis.get("readme", "").lower()
        issues = []
        if "install" not in readme:
            issues.append("Missing installation instructions.")
        if not analysis.get("tech_files"):
            issues.append("Tech stack files not found.")
        if not any("usage" in line.lower() for line in readme.splitlines()):
            issues.append("Missing usage instructions.")
        return issues or ["No critical issues found."]

class FixerAgent(ConversableAgent):
    def debate(self, issues):
        suggestions = []
        for issue in issues:
            if "install" in issue:
                suggestions.append("Suggest adding a step-by-step install guide under README.")
            elif "usage" in issue:
                suggestions.append("Suggest adding sample usage commands to demonstrate functionality.")
            elif "tech stack" in issue:
                suggestions.append("Add a requirements.txt or package.json to define dependencies.")
        return suggestions

class IssueAgent(ConversableAgent):
    def create_issues(self, repo, issues, suggestions):
        formatted = []
        for i, (issue, fix) in enumerate(zip(issues, suggestions), 1):
            title = issue.split(".")[0]
            body = f"Issue {i}: {issue}\n\nSuggestion: {fix}"
            formatted.append({
                "title": title,
                "body": body,
                "repo": repo
            })
        return formatted

    def open_github_issues(self, formatted_issues):
        created = []
        for issue in formatted_issues:
            url = f"https://api.github.com/repos/{issue['repo']}/issues"
            res = requests.post(url, headers=HEADERS, json={"title": issue["title"], "body": issue["body"]})
            if res.status_code == 201:
                created.append(f"Issue '{issue['title']}' created.")
            else:
                created.append(f"Failed to create issue: {res.text}")
        return created
