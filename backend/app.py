import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

sys.path.insert(0, os.path.dirname(__file__))
from models import init_db, upsert_repo, query_repos, query_recent, get_categories, get_stats
from categorizer import categorize_repo
from description_generator import generate_chinese_description
from github_fetcher import fetch_starred_repos

app = Flask(__name__)
CORS(app)

GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "mraing")


@app.route("/api/repos", methods=["GET"])
def get_repos():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 12, type=int)
    search = request.args.get("search", "", type=str)
    category = request.args.get("category", "", type=str)
    sort = request.args.get("sort", "starred_at", type=str)
    return jsonify(query_repos(page=page, page_size=page_size, search=search, category=category, sort=sort))


@app.route("/api/repos/recent", methods=["GET"])
def get_recent():
    limit = request.args.get("limit", 10, type=int)
    return jsonify(query_recent(limit=limit))


@app.route("/api/categories", methods=["GET"])
def get_categories_route():
    return jsonify(get_categories())


@app.route("/api/repos/stats", methods=["GET"])
def get_stats_route():
    return jsonify(get_stats())


@app.route("/api/repos/refresh", methods=["POST"])
def refresh_repos():
    try:
        repos = fetch_starred_repos(GITHUB_USERNAME)
        count = 0
        for repo in repos:
            category = categorize_repo(repo)
            repo["category"] = category
            repo["chinese_description"] = generate_chinese_description(repo, category)
            upsert_repo(repo)
            count += 1

        return jsonify({"success": True, "count": count, "message": f"成功同步 {count} 个仓库"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/config", methods=["GET"])
def get_config():
    return jsonify({"github_username": GITHUB_USERNAME})


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5001)
