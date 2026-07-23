# 阶段 1 — 基础设施 + 数据注入

## 目标
打通 Supabase → pgvector → RAG 检索 → Chat API 的完整链路

## 任务清单

### 1.1 Supabase 数据库初始化
- [ ] 确认 Supabase 项目中已安装 pgvector 扩展
- [ ] 在 Supabase SQL Editor 中创建 3 张表（persona_dimensions, interests, life_events）
- [ ] 在 Supabase SQL Editor 中创建 3 个 RPC 函数（match_persona_dimensions, match_interests, match_life_events）
- [ ] 验证表结构和 RPC 函数创建成功

### 1.2 数据注入
- [ ] 安装 Python 依赖（sentence-transformers, pgvector, supabase-py 等）
- [ ] 运行 `python -m app.retrieval.ingest` 将 YAML 数据向量化写入 Supabase
- [ ] 验证三张表中各有正确数量的记录

### 1.3 后端启动
- [ ] 确认 .env 配置正确（DATABASE_URL, SUPABASE_URL, SUPABASE_ANON_KEY, DEEPSEEK_API_KEY）
- [ ] 启动 FastAPI: `uvicorn app.main:app --reload --port 8000`
- [ ] 验证 `/health` 端点正常
- [ ] 验证 `/api/chat` 端点可响应

### 1.4 前端对接
- [ ] 启动 Next.js: `npm run dev`
- [ ] 验证首页 `/` 正常显示
- [ ] 测试 `/chat` 页面发送消息
- [ ] 确认 SSE 流式对话正常工作

## 验收标准
1. ❓ 输入"你喜欢什么音乐？" → 返回有关兴趣爱好的回答
2. ❓ 输入"你的 MBTI 是什么？" → 返回 ISTP 相关描述
3. 对话流式输出，不卡顿
4. 不能出现"根据我的数据"等出戏表述
