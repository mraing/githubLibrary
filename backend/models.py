import sqlite3
import os
import json

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DB_PATH = os.path.join(DB_DIR, "github_library.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS repositories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            github_id INTEGER UNIQUE NOT NULL,
            name TEXT NOT NULL,
            full_name TEXT NOT NULL,
            html_url TEXT NOT NULL,
            description TEXT,
            chinese_description TEXT,
            category TEXT NOT NULL DEFAULT '其他',
            language TEXT,
            topics TEXT,
            stargazers_count INTEGER DEFAULT 0,
            starred_at TEXT NOT NULL,
            created_at TEXT,
            updated_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def upsert_repo(repo: dict):
    conn = get_db()
    topics = repo.get("topics")
    if isinstance(topics, list):
        topics = json.dumps(topics, ensure_ascii=False)
    conn.execute("""
        INSERT INTO repositories (github_id, name, full_name, html_url, description,
            chinese_description, category, language, topics, stargazers_count,
            starred_at, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(github_id) DO UPDATE SET
            name=excluded.name,
            full_name=excluded.full_name,
            html_url=excluded.html_url,
            description=excluded.description,
            chinese_description=excluded.chinese_description,
            category=excluded.category,
            language=excluded.language,
            topics=excluded.topics,
            stargazers_count=excluded.stargazers_count,
            starred_at=excluded.starred_at,
            updated_at=excluded.updated_at
    """, (
        repo["github_id"], repo["name"], repo["full_name"], repo["html_url"],
        repo.get("description"), repo.get("chinese_description"), repo["category"],
        repo.get("language"), topics, repo.get("stargazers_count", 0),
        repo["starred_at"], repo.get("created_at"), repo.get("updated_at")
    ))
    conn.commit()
    conn.close()


def query_repos(page=1, page_size=12, search="", category="", sort="starred_at"):
    conn = get_db()
    conditions = []
    params = []

    if search:
        conditions.append("(name LIKE ? OR full_name LIKE ? OR description LIKE ? OR chinese_description LIKE ?)")
        kw = f"%{search}%"
        params.extend([kw, kw, kw, kw])

    if category:
        if category == "最近关注":
            # 最近关注：按 starred_at 降序取前 N 条，不走普通分页
            pass
        else:
            conditions.append("category = ?")
            params.append(category)

    where = " WHERE " + " AND ".join(conditions) if conditions else ""

    count_sql = f"SELECT COUNT(*) FROM repositories{where}"
    count = conn.execute(count_sql, params).fetchone()[0]

    sort_map = {"starred_at": "starred_at DESC", "stars": "stargazers_count DESC", "name": "name ASC"}
    order = sort_map.get(sort, "starred_at DESC")

    offset = (page - 1) * page_size
    data_sql = f"SELECT * FROM repositories{where} ORDER BY {order} LIMIT ? OFFSET ?"
    rows = conn.execute(data_sql, params + [page_size, offset]).fetchall()
    conn.close()

    repos = [dict(r) for r in rows]
    return {"items": repos, "total": count, "page": page, "page_size": page_size}


def query_recent(limit=10):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM repositories ORDER BY starred_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_categories():
    conn = get_db()
    rows = conn.execute(
        "SELECT category, COUNT(*) as count FROM repositories GROUP BY category ORDER BY count DESC"
    ).fetchall()
    conn.close()
    return [{"name": r["category"], "count": r["count"]} for r in rows]


def get_stats():
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM repositories").fetchone()[0]
    total_stars = conn.execute("SELECT SUM(stargazers_count) FROM repositories").fetchone()[0] or 0
    langs = conn.execute(
        "SELECT language, COUNT(*) as count FROM repositories WHERE language != '' GROUP BY language ORDER BY count DESC LIMIT 10"
    ).fetchall()
    conn.close()
    return {
        "total_repos": total,
        "total_stars": total_stars,
        "top_languages": [{"language": l["language"], "count": l["count"]} for l in langs]
    }
