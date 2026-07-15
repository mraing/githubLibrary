def generate_chinese_description(repo: dict, category: str) -> str:
    name = repo.get("name", "")
    desc = (repo.get("description") or "").lower()
    lang = repo.get("language") or ""
    topics = repo.get("topics", [])
    if isinstance(topics, str):
        import json
        try:
            topics = json.loads(topics)
        except json.JSONDecodeError:
            topics = []
    full_name = repo.get("full_name", "")

    parts = []

    if any(t in topics for t in ["awesome", "awesome-list"]):
        return f"这是一份精心整理的资源列表，收录了 {name.replace('-', ' ')} 相关的优质项目、工具和资料，帮助开发者高效地找到所需资源。可用于技术选型、学习参考或构建自己的工具链。"

    if "framework" in desc or "framework" in topics:
        parts.append(f"{name} 是一个开发框架")
    elif "library" in desc or "lib" in topics:
        parts.append(f"{name} 是一个代码库")
    elif "tool" in desc or "tool" in topics:
        parts.append(f"{name} 是一个实用工具")
    elif "cli" in desc or "cli" in topics:
        parts.append(f"{name} 是一个命令行工具")
    elif "sdk" in desc:
        parts.append(f"{name} 是一个 SDK / 开发套件")
    elif "plugin" in desc or "plugin" in topics or "extension" in desc:
        parts.append(f"{name} 是一个插件 / 扩展")
    elif "template" in desc:
        parts.append(f"{name} 是一个项目模板")
    elif "demo" in desc or "example" in desc:
        parts.append(f"{name} 是一个示例 / 演示项目")
    elif "tutorial" in desc or "guide" in desc or "course" in desc:
        parts.append(f"{name} 是一份教程 / 指南")
    elif "book" in desc:
        parts.append(f"{name} 是一本开源书籍")
    else:
        parts.append(f"{name} 是一个开源项目")

    if category == "AI / 机器学习":
        if "llm" in desc or "gpt" in desc or "agent" in desc:
            parts.append(f"专注于大语言模型 (LLM) 和 AI 智能体开发")
        elif "inference" in desc:
            parts.append(f"提供高效的模型推理能力")
        elif "rag" in desc:
            parts.append(f"实现检索增强生成 (RAG) 技术栈")
        elif "embedding" in desc:
            parts.append(f"提供文本 / 向量嵌入能力")
        elif "pytorch" in desc or "tensorflow" in desc:
            parts.append(f"基于主流深度学习框架构建")
        else:
            parts.append(f"涉及人工智能与机器学习领域")
    elif category == "前端开发":
        if "react" in desc or "react" in topics:
            parts.append(f"基于 React 构建")
        elif "vue" in desc or "vue" in topics:
            parts.append(f"基于 Vue.js 构建")
        elif "component" in desc:
            parts.append(f"提供高质量的 UI 组件")
        elif "css" in desc:
            parts.append(f"专注于样式和视觉呈现")
        else:
            parts.append(f"用于前端用户界面开发")
    elif category == "后端开发":
        if "api" in desc:
            parts.append(f"提供 RESTful / GraphQL API 服务")
        elif "database" in desc:
            parts.append(f"涉及数据库管理与优化")
        else:
            parts.append(f"用于后端服务与数据处理")
    elif category == "开发工具":
        parts.append(f"提升开发效率和工程体验")
    elif category == "数据结构与算法":
        parts.append(f"帮助提升算法能力和编程思维")
    elif category == "文档教程":
        parts.append(f"为开发者提供学习参考和知识整理")
    elif category == "Skills":
        if "mcp" in desc or "mcp" in topics:
            parts.append(f"基于 MCP (Model Context Protocol) 协议扩展 AI 能力边界")
        elif "browser" in desc or "harness" in desc:
            parts.append(f"提供浏览器自动化与智能操控能力")
        elif "skill" in desc or "skill" in name.lower():
            parts.append(f"为 AI 编程助手注入专业领域知识与工作流")
        else:
            parts.append(f"增强 AI 助手的工具调用和自动化能力")
    elif category == "移动开发":
        parts.append(f"面向移动端应用开发场景")

    lang_map = {
        "Go": "使用 Go 语言开发", "Python": "使用 Python 编写", "Rust": "使用 Rust 语言构建",
        "TypeScript": "基于 TypeScript", "JavaScript": "基于 JavaScript",
        "Java": "使用 Java 开发", "Kotlin": "使用 Kotlin 编写", "Swift": "使用 Swift 开发",
        "C++": "使用 C++ 编写", "C": "使用 C 语言编写", "C#": "使用 C# 开发",
        "Ruby": "使用 Ruby 编写", "PHP": "使用 PHP 开发", "Zig": "使用 Zig 语言构建",
        "Dart": "使用 Dart 语言编写",
    }
    if lang in lang_map:
        parts.append(lang_map[lang])

    scenes = []
    if category == "AI / 机器学习":
        scenes.append("适用于需要集成 AI 能力的应用场景")
        scenes.append("如智能客服、代码生成、内容创作、知识问答等")
    elif category == "前端开发":
        scenes.append("适用于 Web 应用、后台管理系统或 H5 页面开发")
    elif category == "后端开发":
        scenes.append("适用于构建 API 服务、微服务架构或数据处理管线")
    elif category == "开发工具":
        scenes.append("适用于日常开发提效、自动化流程或 CI/CD 管线")
    elif category == "数据结构与算法":
        scenes.append("适用于面试准备、算法练习和编程竞赛")
    elif category == "移动开发":
        scenes.append("适用于 iOS / Android 应用开发")
    elif category == "文档教程":
        scenes.append("适用于技术学习、查阅和团队知识沉淀")
    elif category == "Skills":
        scenes.append("适用于扩展 AI 编程助手的能力边界")
        scenes.append("如自动化工作流、浏览器操控、代码智能分析等")

    result = "，".join(parts)
    if scenes:
        result += "。" + "；".join(scenes) + "。"

    if len(result) < 40:
        result += f" 可从 {full_name} 获取更多信息。"

    return result
