import requests

def analyze_repo(repo_url):
    # crude heuristic to get README
    user_repo = "/".join(repo_url.split("/")[-2:])
    api_url = f"https://api.github.com/repos/{user_repo}/readme"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    res = requests.get(api_url, headers=headers)
    readme = res.text

    # Extract install or usage lines
    lines = [l for l in readme.splitlines() if "install" in l.lower() or "$" in l or "usage" in l.lower()]
    return "\n".join(lines[:10])
