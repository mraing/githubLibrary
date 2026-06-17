import { Input } from "antd";
import { SearchOutlined } from "@ant-design/icons";

export default function SearchBar({ value, onChange }) {
  return (
    <Input
      allowClear
      size="large"
      placeholder="搜索仓库名称、描述..."
      prefix={<SearchOutlined style={{ color: "#aeaeb2" }} />}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      style={{
        width: 340,
        borderRadius: 12,
        background: "#fff",
        border: "1px solid transparent",
        boxShadow: "0 1px 3px rgba(0,0,0,0.04)",
      }}
    />
  );
}
