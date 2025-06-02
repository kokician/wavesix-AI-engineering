import os
import requests
from utils.github_utils import extract_user_repo

class IssueCollectorAgent:
    def __init__(self, repo_url, memory):
        self.repo_url = repo_url
        self.memory = memory
        self.headers = {
            "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
            "Accept": "application/vnd.github.v3+json"
        }

    def run(self):
        user_repo = extract_user_repo(self.repo_url)
        api_url = f"https://api.github.com/repos/{user_repo}/issues"
        res = requests.get(api_url, headers=self.headers)
        issues = res.json()
        summaries = []
        for issue in issues:
            if 'pull_request' not in issue:
                summary = f"{issue['title']} - {issue.get('body', '')[:100]}"
                self.memory.save_context({"input": issue['title']}, {"output": summary})
                summaries.append(summary)
        return summaries
