from urllib.parse import urlparse

def extract_user_repo(repo_url):
    """Extracts 'user/repo' from a full GitHub URL."""
    path_parts = urlparse(repo_url).path.strip("/").split("/")
    if len(path_parts) >= 2:
        return f"{path_parts[0]}/{path_parts[1]}"
    raise ValueError("Invalid GitHub repository URL")
