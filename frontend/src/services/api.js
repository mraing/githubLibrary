const BASE = "/api";

export async function fetchRepos({ page = 1, pageSize = 12, search = "", category = "", sort = "starred_at" } = {}) {
  const params = new URLSearchParams({ page, page_size: pageSize, sort });
  if (search) params.set("search", search);
  if (category) params.set("category", category);
  const resp = await fetch(`${BASE}/repos?${params}`);
  if (!resp.ok) throw new Error("Failed to fetch repos");
  return resp.json();
}

export async function fetchRecentRepos(limit = 10) {
  const resp = await fetch(`${BASE}/repos/recent?limit=${limit}`);
  if (!resp.ok) throw new Error("Failed to fetch recent repos");
  return resp.json();
}

export async function fetchCategories() {
  const resp = await fetch(`${BASE}/categories`);
  if (!resp.ok) throw new Error("Failed to fetch categories");
  return resp.json();
}

export async function fetchStats() {
  const resp = await fetch(`${BASE}/repos/stats`);
  if (!resp.ok) throw new Error("Failed to fetch stats");
  return resp.json();
}

export async function refreshRepos() {
  const resp = await fetch(`${BASE}/repos/refresh`, { method: "POST" });
  if (!resp.ok) {
    const err = await resp.json();
    throw new Error(err.message || "Refresh failed");
  }
  return resp.json();
}
