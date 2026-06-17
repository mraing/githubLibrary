GitHub 图书馆

目的：创建一个前端项目,用于展示我的关注的仓库列表。
你需要使用Python将我的GitHub仓库中的关注的仓库列表提取出来，然后将这些仓库的名称和URL写入到一个JSON文件中，然后使用HTML和CSS以及index.html文件，用于展示这些仓库的名称和URL。

这里我想和你讨论下，是将数据存储到JSON文件中好，还是放到数据库中比较好？

功能描述：
1. 从我的GitHub仓库中提取关注的仓库列表。
2. 将提取到的仓库列表写入到一个JSON文件中。
3. 使用HTML和CSS创建一个index.html文件，用于展示这些仓库的名称和URL。
4. 在index.html文件中，使用JSON文件中的数据，动态生成一个列表，用于展示这些仓库的名称和URL。

需要注意的事情：
1. 对仓库进行分类，比如前端类，AI类，工具类等等，具体怎么分类，由你来决定。
2. 搜索功能：能够根据仓库的名称或URL进行搜索。
3. 分类功能：能够根据仓库的分类进行筛选；以及一个分页功能，能够将仓库列表分页展示。
4. 还需要有一个类型，用于展示最近关注的仓库。
5. 对仓库进行说明和描述（必须使用中文），让我一眼就知道这个仓库是干嘛，它能做什么，我能在什么场景中能用到它。
6. 每个仓库可以做成卡片的样式，每个卡片包含仓库的名称、跳转到仓库GitHub URL的链接、分类、说明和描述。

前端框架使用 react + antd 组件库。
python 你可以使用 flask 框架。
数据库可以使用 sqlite。


1. 启动后端

cd /Users/xufeng/Documents/github_library
GITHUB_USERNAME=mraing python backend/app.py
后端运行在 http://localhost:5001。

2. 启动前端

cd /Users/xufeng/Documents/github_library/frontend
npm run dev
前端运行在 http://localhost:5173，API 请求自动代理到后端。