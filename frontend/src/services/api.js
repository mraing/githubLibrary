const DATA_URL = "/data/all.json";

let _cache = null;

async function loadData() {
  if (_cache) return _cache;
  const resp = await fetch(DATA_URL);
  if (!resp.ok) throw new Error("Failed to load repo data");
  const json = await resp.json();
  _cache = json.repos || json;
  return _cache;
}

export async function fetchRepos({ page = 1, pageSize = 12, search = "", category = "", sort = "starred_at" } = {}) {
  const repos = await loadData();
  let filtered = [...repos];

  if (category) {
    filtered = filtered.filter((r) => r.category === category);
  }

  if (search) {
    const q = search.toLowerCase();
    filtered = filtered.filter(
      (r) =>
        (r.name && r.name.toLowerCase().includes(q)) ||
        (r.full_name && r.full_name.toLowerCase().includes(q)) ||
        (r.description && r.description.toLowerCase().includes(q)) ||
        (r.chinese_description && r.chinese_description.toLowerCase().includes(q))
    );
  }

  const sortMap = {
    starred_at: (a, b) => (b.starred_at || "").localeCompare(a.starred_at || ""),
    stars: (a, b) => b.stargazers_count - a.stargazers_count,
    name: (a, b) => (a.name || "").localeCompare(b.name || ""),
  };
  filtered.sort(sortMap[sort] || sortMap.starred_at);

  const total = filtered.length;
  const start = (page - 1) * pageSize;
  const items = filtered.slice(start, start + pageSize);

  return { items, total, page, page_size: pageSize };
}

export async function fetchRecentRepos(limit = 10) {
  const repos = await loadData();
  const sorted = [...repos].sort((a, b) => (b.starred_at || "").localeCompare(a.starred_at || ""));
  return sorted.slice(0, limit);
}

export async function fetchCategories() {
  const repos = await loadData();
  const map = {};
  for (const r of repos) {
    const cat = r.category || "其他";
    map[cat] = (map[cat] || 0) + 1;
  }
  return Object.entries(map)
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count);
}

export async function fetchStats() {
  const repos = await loadData();
  const total = repos.length;
  const totalStars = repos.reduce((sum, r) => sum + (r.stargazers_count || 0), 0);
  const langMap = {};
  for (const r of repos) {
    if (r.language) {
      langMap[r.language] = (langMap[r.language] || 0) + 1;
    }
  }
  const topLanguages = Object.entries(langMap)
    .map(([language, count]) => ({ language, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 10);
  return { total_repos: total, total_stars: totalStars, top_languages: topLanguages };
}

export async function refreshRepos() {
  throw new Error("数据由 GitHub Actions 每日自动更新，无需手动刷新");
}
