# GitHub 图书馆

将你 GitHub 上 Star 的仓库整理成带分类、搜索、中文描述的知识库。

## 功能

- **自动同步** — 从 GitHub Starred API 拉取你所有 Star 的仓库
- **智能分类** — 根据仓库描述、语言、Topics 自动归类（AI / 机器学习、前端开发、后端开发、开发工具等）
- **中文描述** — 为每个仓库自动生成中文说明，一眼看懂用途和适用场景
- **搜索** — 按仓库名、全名、描述、中文描述实时搜索
- **分类筛选** — 按类别筛选，含「最近关注」快速入口
- **分页** — 卡片网格展示，支持分页
- **统计** — 仓库总数、Star 总数、Top 语言分布

## 截图

| 首页概览 | 分类筛选 | 搜索 |
|---------|---------|------|
| 卡片网格展示最近关注和所有仓库 | 分类 pill 切换，实时过滤 | 按名称/描述搜索，防抖查询 |

## 技术栈

| 层 | 技术 |
|---|------|
| 前端 | React 19 + Ant Design 5 + Vite 6 |
| 后端 | Python + Flask |
| 数据库 | SQLite（本地文件） |
| 数据源 | GitHub Starred API |

## 快速开始

### 前置要求

- Python 3.9+
- Node.js 18+
- npm

### 1. 后端

```bash
# 安装依赖
pip install flask flask-cors requests

# 设置 GitHub 用户名（必填）
export GITHUB_USERNAME=your_github_username
# 建议设置 Token 以提高 API 速率限制（不需要任何权限）
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# 启动（默认端口 5001）
python backend/app.py
```

首次启动数据库为空，需要点击页面上方的「刷新」按钮同步数据，或直接调用 API：

```bash
curl -X POST http://localhost:5001/api/repos/refresh
```

### 2. 前端

```bash
cd frontend
npm install
npm run dev
```

前端运行在 `http://localhost:5173`，Vite 自动将 `/api` 请求代理到后端。

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `GITHUB_USERNAME` | 是 | 要同步的 GitHub 用户名 |
| `GITHUB_TOKEN` | 否 | GitHub Personal Access Token，未设置时匿名请求（60 次/小时），设置后 5000 次/小时 |

## API

基础路径：`http://localhost:5001/api`

### `GET /api/repos`

获取仓库列表（分页、搜索、筛选、排序）。

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `page` | int | 1 | 页码 |
| `page_size` | int | 12 | 每页数量 |
| `search` | string | — | 搜索关键词（匹配 name / full_name / description / chinese_description） |
| `category` | string | — | 分类名称（为空时返回全部） |
| `sort` | string | `starred_at` | 排序字段：`starred_at`（收藏时间）、`stars`（Star 数）、`name`（名称） |

### `GET /api/repos/recent`

最近关注的仓库。

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `limit` | int | 10 | 返回数量 |

### `GET /api/categories`

获取所有分类及每个分类下的仓库数量。

### `GET /api/repos/stats`

获取统计信息：仓库总数、Star 总数、Top 语言分布。

### `POST /api/repos/refresh`

从 GitHub 重新同步所有 Starred 仓库（覆盖已有数据）。

### `GET /api/config`

获取当前配置（如 `github_username`）。

## 分类规则

仓库根据以下优先级自动分类：

1. **关键词匹配** — 描述或 Topics 中包含特定关键词（如 `llm` → AI / 机器学习）
2. **Topics 匹配** — GitHub Topics 匹配分类规则
3. **语言匹配** — 根据编程语言推断分类（如 Swift → 移动开发）
4. **兜底** — 以上均不匹配归入「其他」

当前分类：Skills、AI / 机器学习、前端开发、后端开发、开发工具、移动开发、数据结构与算法、文档教程、其他。

分类规则在 [backend/categorizer.py](backend/categorizer.py) 中配置。

## 项目结构

```
github_library/
├── backend/
│   ├── app.py              # Flask 后端入口与路由
│   ├── models.py           # SQLite 数据库模型与查询
│   ├── github_fetcher.py   # GitHub Starred API 调用
│   └── categorizer.py      # 仓库自动分类规则
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx       # 顶栏（刷新按钮）
│   │   │   ├── SearchBar.jsx    # 搜索输入框
│   │   │   ├── CategoryFilter.jsx  # 分类筛选 pill
│   │   │   ├── RepoCard.jsx     # 仓库卡片
│   │   │   ├── RepoGrid.jsx     # 卡片网格 + 分页
│   │   │   └── RecentRepos.jsx  # 最近关注横向滚动区
│   │   ├── services/
│   │   │   └── api.js           # API 请求封装
│   │   ├── App.jsx              # 主应用组件
│   │   └── main.jsx             # 入口
│   ├── vite.config.js           # Vite 配置（含 API 代理）
│   └── package.json
├── data/                        # SQLite 数据库文件目录（自动创建）
└── README.md
```
