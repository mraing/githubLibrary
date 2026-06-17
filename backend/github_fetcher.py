import requests
import time
import os

GITHUB_API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN") or ""


def _headers():
    h = {"Accept": "application/vnd.github.star+json"}
    if TOKEN:
        h["Authorization"] = f"token {TOKEN}"
    return h


def fetch_starred_repos(username: str) -> list[dict]:
    """Fetch all starred repos for a given user. Returns list of repo dicts."""
    repos = []
    page = 1
    per_page = 100

    while True:
        url = f"{GITHUB_API}/users/{username}/starred?page={page}&per_page={per_page}"
        resp = requests.get(url, headers=_headers())

        if resp.status_code == 403:
            remaining = int(resp.headers.get("X-RateLimit-Remaining", 0))
            if remaining == 0:
                reset_at = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
                wait = max(reset_at - time.time() + 5, 1)
                print(f"速率限制，等待 {wait:.0f} 秒...")
                time.sleep(wait)
                continue
            else:
                raise Exception(f"GitHub API 403: {resp.text}")

        if resp.status_code != 200:
            raise Exception(f"GitHub API 错误 {resp.status_code}: {resp.text}")

        data = resp.json()
        if not data:
            break

        for item in data:
            # starred_at 在 starred API 返回中
            starred = item.get("starred_at", "")
            repo = item.get("repo", item)
            repos.append({
                "github_id": repo["id"],
                "name": repo["name"],
                "full_name": repo["full_name"],
                "html_url": repo["html_url"],
                "description": repo.get("description") or "",
                "language": repo.get("language") or "",
                "topics": repo.get("topics", []),
                "stargazers_count": repo.get("stargazers_count", 0),
                "starred_at": starred,
                "created_at": repo.get("created_at", ""),
                "updated_at": repo.get("updated_at", ""),
            })

        page += 1
        time.sleep(0.1)  # 温和速率控制

    return repos
