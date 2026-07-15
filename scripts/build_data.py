"""Generate static JSON data from GitHub starred repos.

Usage:
    python scripts/build_data.py

Env vars:
    GH_USERNAME — GitHub username to fetch stars for
    GITHUB_TOKEN    — (optional) GitHub personal access token for higher rate limits
"""

import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
from github_fetcher import fetch_starred_repos
from categorizer import categorize_repo
from description_generator import generate_chinese_description

USERNAME = os.environ.get("GH_USERNAME", "mraing")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend", "public", "data")


def main():
    print(f"Fetching starred repos for {USERNAME} ...")
    repos = fetch_starred_repos(USERNAME)
    print(f"Fetched {len(repos)} repos")

    for repo in repos:
        repo["category"] = categorize_repo(repo)
        repo["chinese_description"] = generate_chinese_description(repo, repo["category"])
        repo["id"] = repo["github_id"]

    # Sort by starred_at descending
    repos.sort(key=lambda r: r.get("starred_at", ""), reverse=True)

    os.makedirs(DATA_DIR, exist_ok=True)

    output = {
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repos": repos,
    }

    output_path = os.path.join(DATA_DIR, "all.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False)

    print(f"Written {len(repos)} repos to {output_path}")

    # Print category breakdown
    cats = {}
    for r in repos:
        c = r["category"]
        cats[c] = cats.get(c, 0) + 1
    print("Categories:")
    for name, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {name}: {count}")


if __name__ == "__main__":
    main()
