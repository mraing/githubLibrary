import { useState, useEffect, useCallback, useRef } from "react";
import { Layout, ConfigProvider, theme } from "antd";
import zhCN from "antd/locale/zh_CN";
import { fetchRepos, fetchRecentRepos, fetchCategories, refreshRepos } from "./services/api";
import Header from "./components/Header";
import SearchBar from "./components/SearchBar";
import CategoryFilter from "./components/CategoryFilter";
import RepoGrid from "./components/RepoGrid";
import RecentRepos from "./components/RecentRepos";
import "./App.css";

const { Content } = Layout;

export default function App() {
  const [repos, setRepos] = useState([]);
  const [recent, setRecent] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [pagination, setPagination] = useState({
    page: 1,
    pageSize: 12,
    total: 0,
  });

  const debounceRef = useRef(null);

  const loadData = useCallback(async (page, cat, q) => {
    setLoading(true);
    try {
      if (cat === "最近关注") {
        const data = await fetchRecentRepos(12);
        setRepos(data);
        setPagination((p) => ({ ...p, total: data.length, page: 1 }));
      } else {
        const data = await fetchRepos({
          page,
          pageSize: 12,
          search: q,
          category: cat,
        });
        setRepos(data.items);
        setPagination((p) => ({ ...p, total: data.total, page: data.page }));
      }
    } catch (e) {
      console.error("加载仓库失败:", e);
    } finally {
      setLoading(false);
    }
  }, []);

  const loadRecent = useCallback(async () => {
    try {
      const data = await fetchRecentRepos(10);
      setRecent(data);
    } catch (e) {
      console.error("加载最近关注失败:", e);
    }
  }, []);

  const loadCategories = useCallback(async () => {
    try {
      const data = await fetchCategories();
      setCategories(data);
    } catch (e) {
      console.error("加载分类失败:", e);
    }
  }, []);

  useEffect(() => {
    loadCategories();
    loadRecent();
    loadData(1, "", "");
  }, []);

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      if (category === "最近关注") setCategory("");
      loadData(1, category, search);
    }, 300);
    return () => clearTimeout(debounceRef.current);
  }, [search]);

  useEffect(() => {
    setSearch("");
    loadData(1, category, "");
  }, [category]);

  const handleRefresh = useCallback(async () => {
    setRefreshing(true);
    try {
      await refreshRepos();
      await Promise.all([loadCategories(), loadRecent()]);
      setCategory("");
      setSearch("");
      loadData(1, "", "");
    } finally {
      setRefreshing(false);
    }
  }, [loadCategories, loadRecent, loadData]);

  const showRecent = category === "" && !search && pagination.page === 1;

  return (
    <ConfigProvider
      locale={zhCN}
      theme={{
        algorithm: theme.defaultAlgorithm,
        token: {
          colorPrimary: "#1d1d1f",
          colorBgContainer: "#fff",
          borderRadius: 10,
          fontFamily: `-apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", "PingFang SC", sans-serif`,
        },
      }}
    >
      <Layout style={{ minHeight: "100vh", background: "#f5f5f7" }}>
        <Header onRefresh={handleRefresh} loading={refreshing} />
        <Content
          style={{
            padding: "36px 48px",
            maxWidth: 1400,
            margin: "0 auto",
            width: "100%",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "flex-start",
              flexWrap: "wrap",
              gap: 20,
              marginBottom: 36,
            }}
          >
            <SearchBar value={search} onChange={setSearch} />
            <CategoryFilter
              categories={categories}
              active={category}
              onChange={setCategory}
            />
          </div>

          {showRecent && <RecentRepos repos={recent} loading={false} />}

          <RepoGrid
            repos={repos}
            loading={loading}
            pagination={pagination}
            onPageChange={(page) => loadData(page, category, search)}
          />
        </Content>
      </Layout>
    </ConfigProvider>
  );
}
