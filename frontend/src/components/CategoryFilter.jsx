import { ClockCircleOutlined } from "@ant-design/icons";

const base = {
  display: "inline-flex",
  alignItems: "center",
  gap: 5,
  padding: "6px 18px",
  borderRadius: 10,
  border: "none",
  fontSize: 13,
  fontWeight: 540,
  cursor: "pointer",
  background: "transparent",
  color: "#6e6e73",
  transition: "all 0.2s ease",
  fontFamily: "inherit",
  letterSpacing: "-0.01em",
};

const active = {
  ...base,
  background: "#1d1d1f",
  color: "#fff",
};

export default function CategoryFilter({ categories, active: current, onChange }) {
  const pills = [
    { key: "", label: "全部" },
    { key: "最近关注", label: "最近关注", icon: true },
    ...categories.map((c) => ({ key: c.name, label: c.name, count: c.count })),
  ];

  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 6, alignItems: "center" }}>
      {pills.map((p) => (
        <button
          key={p.key}
          style={current === p.key ? active : base}
          onClick={() => onChange(p.key)}
        >
          {p.icon && <ClockCircleOutlined style={{ fontSize: 11 }} />}
          {p.label}
          {p.count !== undefined && (
            <span style={{ opacity: current === p.key ? 0.6 : 0.45, fontSize: 11, fontWeight: 400 }}>
              {p.count}
            </span>
          )}
        </button>
      ))}
    </div>
  );
}
