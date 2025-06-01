import os
import json
import requests
from autogen import ConversableAgent
from dotenv import load_dotenv
from utils.github_utils import extract_user_repo
from memory.vector_memory import save_to_vector_memory, search_vector_memory
from memory.memory_agent import MemoryAgent

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = os.getenv("GITHUB_USERNAME")  
HEADERS = {
    "Accept": "application/vnd.github.v3.raw"
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"


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

class CriticAgent(MemoryAgent):
    def critique(self, repo_url, analysis):
        self.load_memory(repo_url)

        readme = analysis.get("readme", "").lower()
        issues = []
        if "install" not in readme:
            issues.append("Missing installation instructions.")
        if not analysis.get("tech_files"):
            issues.append("Tech stack files not found.")
        if not any("usage" in line.lower() for line in readme.splitlines()):
            issues.append("Missing usage instructions.")

        critique_msg = f"Issues found: {issues or ['None']}"
        self.remember(repo_url, critique_msg)
        return issues or ["No critical issues found."]

class FixerAgent(MemoryAgent):
    def debate(self, repo_url, issues):
        self.load_memory(repo_url)
        suggestions = []
        for issue in issues:
            if "install" in issue:
                suggestions.append("Suggest adding a step-by-step install guide under README.")
            elif "usage" in issue:
                suggestions.append("Suggest adding sample usage commands to demonstrate functionality.")
            elif "tech stack" in issue:
                suggestions.append("Add a requirements.txt or package.json to define dependencies.")
        self.remember(repo_url, f"Suggestions: {suggestions}")
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
            repo = issue['repo']  # 
            print(f"Forking repo: {repo}") 

            # Fork the repo if it is not owned by the user already
            if not repo.startswith(f"{USERNAME}/"):
                fork_resp = requests.post(f"https://api.github.com/repos/{repo}/forks", headers=HEADERS)
                if fork_resp.status_code != 202:
                    created.append(f"Failed to fork repo {repo}: {fork_resp.text}")
                    continue
                forked_repo = f"{USERNAME}/{repo.split('/')[-1]}"
            else:
                forked_repo = repo

    
            url = f"https://api.github.com/repos/{forked_repo}/issues"
            print(f"Creating issue at: {url}")  
            res = requests.post(url, headers=HEADERS, json={"title": issue["title"], "body": issue["body"]})
            if res.status_code == 201:
                created.append(f"Issue '{issue['title']}' created in {forked_repo}.")
            else:
                created.append(f"Failed to create issue in {forked_repo}: {res.text}")

        return created
