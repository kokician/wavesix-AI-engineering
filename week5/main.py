import os
from dotenv import load_dotenv
from agents import RepoAnalyzer, CriticAgent, FixerAgent, IssueAgent

load_dotenv()

analyzer = RepoAnalyzer(name="Analyzer")
critic = CriticAgent(name="Critic")
fixer = FixerAgent(name="Fixer")
issuer = IssueAgent(name="Issuer")

def run_assistant(repo_url):
    analysis = analyzer.analyze(repo_url)
    if isinstance(analysis, str):
        return analysis

    issues = critic.critique(analysis)
    suggestions = fixer.debate(issues)
    issue_list = issuer.create_issues(analysis["repo"], issues, suggestions)
    results = issuer.open_github_issues(issue_list)
    return "\n".join(results)

if __name__ == "__main__":
    print("Multi-Agent GitHub Auditor with Memory + Issue Creation")
    while True:
        user_input = input("Enter GitHub repo URL (or 'exit'): ")
        if user_input.lower() in ['exit', 'quit']:
            break
        output = run_assistant(user_input)
        print("\n=== Assistant Output ===\n")
        print(output)
