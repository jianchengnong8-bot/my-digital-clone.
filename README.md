# 数字分身 (Digital Clone)

一个基于真实人格数据驱动的 AI 数字分身系统。访客可通过人格画像、兴趣标签、人生时间线和 AI 对话，全面了解一个人的性格、爱好和人格特征。

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
│           PostgreSQL + pgvector                    │
│  性格维度 │ 爱好标签 │ 人生事件 │ 对话记录         │
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

### 前端

```bash
npm install
npm run dev
```

### 后端

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 数据库

```bash
docker compose up -d db
```

## 项目结构

```
├── app/                    # Next.js App Router
│   ├── (marketing)/        # 前台展示 (导航栏布局)
│   ├── (dashboard)/        # 后台管理 (侧边栏布局)
│   ├── api/                # API Route (BFF 代理)
│   ├── layout.tsx          # 根布局
│   └── page.tsx            # 首页
├── components/
│   ├── ui/                 # 通用 UI (ScrollReveal, ThemeToggle, NavBar)
│   ├── chart/              # 图表 (DimensionRadar)
│   └── chat/               # 对话 (ChatPanel, ChatBubble)
├── lib/                    # 工具函数 + 数据获取
├── backend/                # FastAPI AI 推理层
│   └── app/
│       ├── api/routes/     # chat, health
│       ├── core/           # config, database
│       ├── agents/         # Agent 编排 (待实现)
│       ├── retrieval/      # RAG 检索 (待实现)
│       └── models/         # Pydantic 数据模型
├── data/                   # 性格数据 (YAML + Prompt 模板)
│   ├── persona/            # 人格维度
│   ├── interests/          # 兴趣爱好
│   ├── timeline/           # 人生事件
│   └── prompts/            # Prompt 模板
├── docker-compose.yml      # PostgreSQL + FastAPI + Next.js
└── Dockerfile              # Next.js standalone 生产构建
```

## 路线图

- [x] 项目骨架搭建 (阶段 0)
- [x] 数据模型定义 (阶段 1)
- [ ] FastAPI RAG 检索实现 (阶段 2)
- [ ] 多 Agent 编排 (阶段 2)
- [ ] 流式对话 SSE (阶段 2)
- [ ] 人格一致性测试 (阶段 5)
- [ ] Docker 全栈部署 (阶段 6)

## 技术栈

| 层级 | 技术 |
|---|---|
| 前端框架 | Next.js 16 (App Router) |
| 可视化 | Recharts + Framer Motion |
| 样式 | Tailwind CSS 4 |
| AI 后端 | Python FastAPI |
| 数据库 | PostgreSQL + pgvector |
| Embedding | BAAI/bge-small-zh-v1.5 |
| LLM | Claude API / GPT API |
