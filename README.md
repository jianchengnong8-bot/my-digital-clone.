# 数字分身 (Digital Clone)

基于真实人格数据驱动的 AI 数字分身系统。访客可通过人格画像、兴趣标签、人生时间线和 AI 对话，全面了解一个人的性格、爱好和人格特征。

## 架构

```
┌──────────────────────────────────────────────────┐
│              前端 (Next.js App Router)             │
│  Server Components + Client Components            │
│  Recharts 可视化 + Framer Motion 动画             │
│  Tailwind CSS 暗色模式                             │
├──────────────────┬───────────────────────────────┤
│  Next.js API Route│     FastAPI (AI 推理层)        │
│  BFF 代理 + 反馈  │     /api/chat 流式对话         │
│                   │     + RAG 检索                  │
│                   │     + 多 Agent 编排              │
├──────────────────┴───────────────────────────────┤
│                   YAML 数据层                       │
│  人格维度 │ 兴趣爱好 │ 人生事件 │ Prompt 模板     │
└──────────────────────────────────────────────────┘
```

## 一键启动

```bash
docker compose up -d
```

- 前端: http://localhost:3000
- 后端 API: http://localhost:8000
- 健康检查: http://localhost:8000/health

## 本地开发

### 前置条件

- Node.js 20+
- Python 3.12+
- Docker（可选，用于容器化部署）

### 前端

```bash
npm install
npm run dev
```

### 后端

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## 项目结构

```
├── app/                    # Next.js App Router
│   ├── (marketing)/        # 前台展示（导航栏布局）
│   │   └── chat/           # AI 对话页
│   ├── (dashboard)/        # 后台管理（侧边栏布局）
│   │   └── admin/          # 管理概览
│   ├── api/                # API Route（BFF 代理）
│   │   ├── chat/           # 对话代理 → FastAPI
│   │   └── feedback/       # 反馈代理 → FastAPI
│   ├── layout.tsx          # 根布局
│   └── page.tsx            # 首页（人格画像 + 时间线）
├── components/
│   ├── ui/                 # 通用 UI（NavBar, ScrollReveal, ThemeToggle）
│   ├── chart/              # 图表（DimensionRadar 雷达图）
│   └── chat/               # 对话（ChatPanel, ChatBubble）
├── lib/                    # 工具函数 + 数据获取
│   ├── utils.ts            # cn(), formatDate(), levelToStars()
│   └── data.ts             # YAML 数据读取层
├── backend/                # FastAPI AI 推理层
│   └── app/
│       ├── api/routes/     # chat（SSE 流）, health
│       ├── core/           # 配置管理
│       ├── agents/         # Agent 编排 + Prompt 构建
│       ├── retrieval/      # BGE Embedding + 内存向量检索
│       └── models/         # Pydantic 数据模型
├── data/                   # 人格数据（YAML + Prompt 模板）
│   ├── persona/            # 人格维度（dimensions.yaml）
│   ├── interests/          # 兴趣爱好（hobbies.yaml）
│   ├── timeline/           # 人生事件（events.yaml）
│   ├── prompts/            # Prompt 模板（system + agents）
│   └── chat_examples.txt   # 对话风格示例
├── docker-compose.yml      # 全栈容器编排
├── Dockerfile              # 前端生产构建
└── backend/Dockerfile      # 后端生产构建
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端框架 | Next.js 16 (App Router + Turbopack) |
| UI 动画 | Framer Motion |
| 图表 | Recharts |
| 样式 | Tailwind CSS 4 |
| AI 后端 | Python FastAPI |
| Agent 编排 | 自研（关键词意图分类 + LLM 流式） |
| Embedding | BAAI/bge-small-zh-v1.5（384 维） |
| 向量检索 | NumPy 内存检索（余弦相似度） |
| LLM | DeepSeek / OpenAI（OpenAI 兼容接口） |

## 路线图

- [x] 项目骨架搭建
- [x] 数据模型定义
- [x] 人格数据录入（5 维度 + 5 兴趣 + 8 事件）
- [x] 前端主页（雷达图 + 兴趣列表 + 时间线）
- [x] AI 对话页（SSE 流式 + Markdown 渲染）
- [x] FastAPI RAG 检索（BGE + NumPy 内存搜索）
- [x] Agent 编排（意图分类 + 模式切换 + 边界检查）
- [x] 流式对话 SSE
- [x] Docker 全栈部署配置
- [ ] 人格一致性自动化测试
- [ ] GitHub Pages 静态展示版
- [ ] 反馈收集与分析
