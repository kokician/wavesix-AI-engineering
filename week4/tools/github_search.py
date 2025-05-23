import requests

def search_github_repos(query):
    headers = {"Accept": "application/vnd.github+json"}
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"
    res = requests.get(url, headers=headers)
    repos = res.json().get("items", [])[:3]
    return "\n".join([f"{r['name']}: {r['html_url']}" for r in repos])
