# 数字分身 (Digital Clone)

## 概述
基于真实人格数据驱动的 AI 数字分身系统。访客可浏览人格画像、兴趣标签、人生时间线，并与 AI 数字人对话。

## 目标
- 让用户通过对话自然了解"农建晟"这个人的性格、经历和想法
- 数据驱动的人格呈现，AI 回复严格遵循人格数据
- 多 Agent 编排，根据用户问题路由到对应专业 Agent
- 完整防出戏系统，保持真实感

## 技术栈
- 前端: Next.js 16 (App Router) + Tailwind CSS 4 + Recharts + Framer Motion
- AI 后端: Python FastAPI + LLM (OpenAI/Anthropic)
- 数据库: Supabase (PostgreSQL + pgvector)
- Embedding: BAAI/bge-small-zh-v1.5
