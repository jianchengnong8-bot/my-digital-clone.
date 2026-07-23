# 需求文档

## 核心功能
1. 人格画像展示 — 5 大维度雷达图 + MBTI + 沟通风格
2. 兴趣爱好展示 — 多级分类浏览
3. 人生时间线 — 按年份展示重要事件
4. AI 对话 — 流式对话，基于人格数据驱动
5. 反馈系统 — 用户对对话质量打分

## 技术需求
1. RAG 检索 — 将 YAML 数据向量化，对话时检索相关片段
2. 多 Agent 编排 — Classifier → (Persona | Interest | Experience)
3. 防出戏系统 — Anti-OOC 防火墙
4. 流式 SSE — Server-Sent Events 流式响应
5. Supabase 持久化 — 对话记录、反馈存储
