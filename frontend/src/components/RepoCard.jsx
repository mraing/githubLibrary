import { Typography } from "antd";
import { StarOutlined, CalendarOutlined } from "@ant-design/icons";
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

const langDot = {
  TypeScript: "#3178c6", JavaScript: "#f0db4f", Python: "#3776ab",
  Go: "#00add8", Rust: "#dea584", Java: "#b07219", Kotlin: "#a97bff",
  Swift: "#f05138", C: "#555", "C++": "#f34b7d", "C#": "#178600",
  Ruby: "#701516", PHP: "#4f5d95", Dart: "#00b4ab", Vue: "#42b883",
  Svelte: "#ff3e00", CSS: "#563d7c", HTML: "#e34c26", Shell: "#89e051",
  Zig: "#ec915c", "Jupyter Notebook": "#da5b0b", MDX: "#1b9",
};

export default function RepoCard({ repo }) {
  const c = categoryShades[repo.category] || categoryShades["其他"];
  const dot = langDot[repo.language] || "#999";

  return (
    <div
      className="repo-card"
      onClick={() => window.open(repo.html_url, "_blank", "noopener")}
      style={{
        background: "#fff",
        borderRadius: 18,
        border: "1px solid transparent",
        padding: "22px 24px",
        cursor: "pointer",
        display: "flex",
        flexDirection: "column",
        height: "100%",
        minHeight: 210,
        transition: "all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1)",
      }}
    >
      {/* 名称 */}
      <Typography.Text
        strong
        ellipsis
        style={{
          fontSize: 15,
          fontWeight: 600,
          color: "#1d1d1f",
          letterSpacing: "-0.01em",
          lineHeight: 1.3,
          marginBottom: 12,
        }}
      >
        {repo.full_name}
      </Typography.Text>

      {/* 标签 */}
      <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 14 }}>
        <span
          style={{
            fontSize: 11,
            fontWeight: 600,
            padding: "3px 9px",
            borderRadius: 6,
            background: c.bg,
            color: c.text,
            letterSpacing: "0.02em",
          }}
        >
          {repo.category}
        </span>
        {repo.language && (
          <span
            style={{
              fontSize: 11,
              fontWeight: 500,
              padding: "3px 9px",
              borderRadius: 6,
              background: "#f5f5f7",
              color: "#6e6e73",
              display: "inline-flex",
              alignItems: "center",
              gap: 5,
            }}
          >
            <span style={{ width: 6, height: 6, borderRadius: 3, background: dot, display: "inline-block", flexShrink: 0 }} />
            {repo.language}
          </span>
        )}
      </div>

      {/* 中文描述 */}
      <Typography.Paragraph
        type="secondary"
        ellipsis={{ rows: 3 }}
        style={{
          flex: 1,
          fontSize: 13,
          lineHeight: 1.7,
          color: "#86868b",
          marginBottom: 0,
        }}
      >
        {repo.chinese_description}
      </Typography.Paragraph>

      {/* 底部 meta */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontSize: 12,
          color: "#aeaeb2",
          borderTop: "1px solid #f5f5f7",
          marginTop: 16,
          paddingTop: 14,
        }}
      >
        <span style={{ display: "flex", alignItems: "center", gap: 5 }}>
          <StarOutlined style={{ fontSize: 11 }} />
          {repo.stargazers_count.toLocaleString()}
        </span>
        <span style={{ display: "flex", alignItems: "center", gap: 5 }}>
          <CalendarOutlined style={{ fontSize: 11 }} />
          {repo.starred_at ? dayjs(repo.starred_at).format("YYYY-MM-DD") : "-"}
        </span>
      </div>
    </div>
  );
}
