import os
import requests

GITHUB_API = "https://api.github.com"


# -----------------------------
# AUTH HEADER
# -----------------------------
def get_headers():
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise Exception("GITHUB_TOKEN not set in environment")

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }


# -----------------------------
# TOOL: LIST REPOS
# -----------------------------
def list_repos():
    """
    Returns all repos accessible to the authenticated user.
    Includes private + public repos depending on token scope.
    """

    url = f"{GITHUB_API}/user/repos"

    params = {
        "visibility": "all",
        "per_page": 100
    }

    response = requests.get(url, headers=get_headers(), params=params)

    if response.status_code != 200:
        return f"GitHub API Error: {response.text}"

    repos = response.json()

    return "\n".join(
        [
            f"{repo['name']} | private={repo['private']} | {repo.get('description')}"
            for repo in repos
        ]
    )


# -----------------------------
# OPTIONAL: GET SINGLE REPO DETAILS
# -----------------------------
def get_repo(owner, repo_name):
    url = f"{GITHUB_API}/repos/{owner}/{repo_name}"

    response = requests.get(url, headers=get_headers())

    if response.status_code != 200:
        return f"GitHub API Error: {response.text}"

    data = response.json()

    return {
        "name": data["name"],
        "description": data.get("description"),
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "language": data.get("language"),
        "updated": data["updated_at"]
    }
