import { Layout, Button, Typography, message } from "antd";
import { ReloadOutlined } from "@ant-design/icons";

const { Header: AntHeader } = Layout;

export default function Header({ onRefresh, loading }) {
  const handleRefresh = async () => {
    try {
      await onRefresh();
      message.success("已刷新仓库数据");
    } catch (e) {
      message.error("刷新失败：" + e.message);
    }
  };

  return (
    <AntHeader
      style={{
        position: "sticky",
        top: 0,
        zIndex: 100,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 48px",
        height: 52,
        background: "rgba(245, 245, 247, 0.72)",
        backdropFilter: "saturate(180%) blur(24px)",
        WebkitBackdropFilter: "saturate(180%) blur(24px)",
        borderBottom: "1px solid rgba(0, 0, 0, 0.06)",
      }}
    >
      <Typography.Text
        strong
        style={{
          fontSize: 16,
          fontWeight: 620,
          color: "#1d1d1f",
          letterSpacing: "-0.02em",
        }}
      >
        GitHub 图书馆
      </Typography.Text>
      <Button
        type="text"
        size="small"
        icon={<ReloadOutlined spin={loading} />}
        onClick={handleRefresh}
        loading={loading}
        style={{ color: "#86868b", fontWeight: 500, fontSize: 13 }}
      >
        刷新
      </Button>
    </AntHeader>
  );
}
