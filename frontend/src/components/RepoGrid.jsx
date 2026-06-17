import { Row, Col, Pagination, Spin, Empty } from "antd";
import RepoCard from "./RepoCard";

export default function RepoGrid({ repos, loading, pagination, onPageChange }) {
  if (loading) {
    return (
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          padding: 120,
        }}
      >
        <Spin size="default" />
      </div>
    );
  }

  if (!repos.length) {
    return (
      <Empty
        description={<span style={{ color: "#86868b" }}>暂无仓库数据</span>}
        style={{ padding: 100 }}
      />
    );
  }

  return (
    <div>
      <Row gutter={[20, 20]}>
        {repos.map((repo) => (
          <Col key={repo.id} xs={24} sm={12} lg={8} xl={6}>
            <RepoCard repo={repo} />
          </Col>
        ))}
      </Row>
      {pagination.total > pagination.pageSize && (
        <div style={{ display: "flex", justifyContent: "center", marginTop: 40 }}>
          <Pagination
            current={pagination.page}
            pageSize={pagination.pageSize}
            total={pagination.total}
            onChange={onPageChange}
            showSizeChanger={false}
            showTotal={(total) => (
              <span style={{ color: "#aeaeb2", fontSize: 13 }}>共 {total} 个</span>
            )}
          />
        </div>
      )}
    </div>
  );
}
