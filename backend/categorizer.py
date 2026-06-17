import json


CATEGORY_RULES = [
    {
        "name": "Skills",
        "keywords": ["skill", "mcp", "browser-harness", "browser-use", "claude", "codex",
                     "cursor", "copilot", "superpower", "codegraph", "playwright-mcp",
                     "cdp", "chrome-devtools", "agent-skill", "agent-harness",
                     "browser-agent", "browser-automation"],
        "topics": ["skill", "mcp", "agent-skills", "ai-agents", "ai-agent", "claude-code",
                   "browser-automation", "browser-harness", "browser-use", "browser-agent",
                   "superpower", "codegraph", "cdp", "chrome-devtools", "playwright-mcp"],
        "languages": []
    },
    {
        "name": "前端开发",
        "keywords": ["typescript", "javascript", "vue", "react", "css", "html", "svelte",
                     "angular", "next.js", "nuxt", "vite", "webpack", "tailwindcss", "component"],
        "topics": ["frontend", "ui", "css", "react", "vue", "component-library", "design-system"],
        "languages": ["TypeScript", "JavaScript", "CSS", "Vue", "Astro", "MDX", "SCSS", "Sass"]
    },
    {
        "name": "后端开发",
        "keywords": ["backend", "server", "api", "rest", "graphql", "microservice", "database",
                     "sql", "postgres", "mysql", "redis", "mongodb", "orm", "message-queue"],
        "topics": ["backend", "server", "api", "database", "rest-api", "grpc"],
        "languages": ["Go", "Python", "Java", "Rust", "C#", "PHP", "Ruby", "Kotlin", "Scala"]
    },
    {
        "keywords": ["skill", "mcp", "browser-harness", "browser-use", "claude", "codex",
                     "cursor", "copilot", "superpower", "codegraph", "playwright-mcp",
                     "cdp", "chrome-devtools", "agent-skill", "agent-harness",
                     "browser-agent", "browser-automation"],
        "topics": ["skill", "mcp", "agent-skills", "ai-agents", "ai-agent", "claude-code",
                   "browser-automation", "browser-harness", "browser-use", "browser-agent",
                   "superpower", "codegraph", "cdp", "chrome-devtools", "playwright-mcp"],
        "languages": []
    },
    {
        "name": "AI / 机器学习",
        "keywords": ["machine-learning", "deep-learning", "transformer",
                     "neural", "nlp", "computer-vision", "ml", "artificial-intelligence",
                     "pytorch", "tensorflow", "model", "inference", "embedding",
                     "rag", "langchain", "prompt", "fine-tune", "diffusion"],
        "topics": ["machine-learning", "llm", "deep-learning", "nlp", "cv", "ml",
                   "artificial-intelligence", "gpt", "rag"],
        "languages": ["Jupyter Notebook", "Python"]
    },
    {
        "name": "开发工具",
        "keywords": ["tool", "cli", "devops", "docker", "kubernetes", "ci", "cd", "testing",
                     "debug", "editor", "ide", "plugin", "extension", "terminal", "shell",
                     "monitoring", "logging", "git", "build", "lint", "formatter"],
        "topics": ["devops", "cli", "tool", "developer-tools", "docker", "testing", "git"],
        "languages": ["Shell", "PowerShell", "Dockerfile", "Makefile"]
    },
    {
        "name": "移动开发",
        "keywords": ["ios", "android", "swift", "kotlin", "flutter", "react-native",
                     "mobile", "app", "wearos"],
        "topics": ["ios", "android", "mobile", "swift", "flutter", "react-native"],
        "languages": ["Swift", "Kotlin", "Dart", "Objective-C"]
    },
    {
        "name": "数据结构与算法",
        "keywords": ["algorithm", "leetcode", "data-structure", "competitive-programming",
                     "coding-interview", "dsa"],
        "topics": ["algorithm", "leetcode", "data-structures", "competitive-programming"],
        "languages": []
    },
    {
        "name": "文档教程",
        "keywords": ["awesome", "tutorial", "guide", "handbook", "roadmap", "interview",
                     "cheatsheet", "collection", "list", "best-practices", "wiki", "doc",
                     "book", "course"],
        "topics": ["awesome-list", "tutorial", "guide", "roadmap", "book", "documentation"],
        "languages": []
    },
]


def categorize_repo(repo: dict) -> str:
    description = (repo.get("description") or "").lower()
    language = repo.get("language") or ""
    topics_list = repo.get("topics") or []
    if isinstance(topics_list, str):
        try:
            topics_list = json.loads(topics_list)
        except json.JSONDecodeError:
            topics_list = []
    topics_str = " ".join(t for t in topics_list if isinstance(t, str)).lower()

    text = f"{description} {topics_str}"

    def rule_matches(rule):
        """Check keyword or topic match — more specific than language."""
        for kw in rule["keywords"]:
            if kw in text:
                return True
        for t in rule["topics"]:
            if t in topics_list:
                return True
        return False

    # Pass 1: keyword / topic match (specific signals take priority)
    for rule in CATEGORY_RULES:
        if rule_matches(rule):
            return rule["name"]

    # Pass 2: language-based fallback (weaker signal)
    for rule in CATEGORY_RULES:
        if language in rule["languages"]:
            return rule["name"]

    return "其他"
