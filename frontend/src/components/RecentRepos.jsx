import { Typography, Spin } from "antd";
import dayjs from "dayjs";

const categoryShades = {
  "Skills":           { bg: "#e8f0fe", text: "#1a56db" },
  "前端开发":          { bg: "#fde8ef", text: "#c0135e" },
  "后端开发":          { bg: "#e6f9ed", text: "#1a7a3a" },
  "AI / 机器学习":     { bg: "#f3e8ff", text: "#6d28d9" },
  "开发工具":          { bg: "#fef3c7", text: "#92400e" },
  "移动开发":          { bg: "#e0f7fa", text: "#0e7490" },
  "数据结构与算法":     { bg: "#ffe4e6", text: "#b91c1c" },
  "文档教程":          { bg: "#ecfdf5", text: "#047857" },
  "其他":              { bg: "#f3f4f6", text: "#6b7280" },
};

export default function RecentRepos({ repos, loading }) {
  if (loading) {
    return <div style={{ textAlign: "center", padding: 40 }}><Spin size="default" /></div>;
  }
  if (!repos.length) return null;

  return (
    <div style={{ marginBottom: 44 }}>
      <Typography.Text
        style={{
          fontSize: 12,
          fontWeight: 600,
          color: "#aeaeb2",
          textTransform: "uppercase",
          letterSpacing: "0.08em",
          display: "block",
          marginBottom: 18,
        }}
      >
        最近关注
      </Typography.Text>
      <div
        style={{
          display: "flex",
          overflowX: "auto",
          gap: 16,
          paddingBottom: 2,
          scrollSnapType: "x mandatory",
        }}
      >
        {repos.map((repo) => {
          const c = categoryShades[repo.category] || categoryShades["其他"];
          return (
            <div
              key={repo.id}
              className="repo-card"
              onClick={() => window.open(repo.html_url, "_blank", "noopener")}
              style={{
                minWidth: 268,
                maxWidth: 310,
                background: "#fff",
                borderRadius: 16,
                border: "1px solid transparent",
                padding: "18px 20px",
                cursor: "pointer",
                flexShrink: 0,
                scrollSnapAlign: "start",
                transition: "all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1)",
              }}
            >
              <Typography.Text
                strong
                ellipsis
                style={{
                  fontSize: 14,
                  fontWeight: 600,
                  color: "#1d1d1f",
                  display: "block",
                  marginBottom: 10,
                }}
              >
                {repo.full_name}
              </Typography.Text>
              <div style={{ display: "flex", gap: 5, marginBottom: 12, flexWrap: "wrap" }}>
                <span style={{ fontSize: 10, fontWeight: 600, padding: "3px 8px", borderRadius: 5, background: c.bg, color: c.text }}>
                  {repo.category}
                </span>
              </div>
              <Typography.Paragraph
                type="secondary"
                ellipsis={{ rows: 2 }}
                style={{ fontSize: 12, color: "#86868b", lineHeight: 1.6, marginBottom: 10 }}
              >
                {repo.chinese_description}
              </Typography.Paragraph>
              <Typography.Text style={{ fontSize: 11, color: "#aeaeb2" }}>
                {repo.starred_at ? dayjs(repo.starred_at).format("YYYY-MM-DD HH:mm") : "-"}
              </Typography.Text>
            </div>
          );
        })}
      </div>
    </div>
  );
}
