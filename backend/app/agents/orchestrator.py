"""
Agent 编排器 — 意图路由 + RAG 检索 + LLM 流式生成

流程:
  用户问题
    → HybridSearcher.search()    # RAG 检索
    → classify_intent()           # 关键词意图分类
    → build_messages()            # 组装 prompt
    → llm_stream()                # 调用 LLM，SSE 流式输出
"""
import asyncio
import json
from typing import AsyncIterator

from openai import AsyncOpenAI

from app.core.config import settings
from app.retrieval.memory_searcher import MemorySearcher
from app.agents.prompt_loader import build_messages, classify_intent

OWNER_NAME = "农建晟"

# 技术相关关键词 — 命中了才允许 RAG 返回编程/项目相关内容
TECH_KEYWORDS = [
    "编程", "代码", "技术", "项目", "开发", "程序员", "软件",
    "AI", "人工智能", "算法", "架构", "前端", "后端", "Python",
    "TypeScript", "Java", "Agent", "RAG", "LLM", "模型",
    "实习", "工作", "职业", "毕业设计", "数字分身",
]

# 需要过滤的标签 — 非技术问题中要排除的结果
TECH_LABELS = [
    "编程与前沿探索",
    "成为优秀的 AI Agent 使用者",
    "启动个人数字分身项目",
    "毕业设计期间接触 AI Agent 技术开发",
]


def _has_tech_intent(query: str) -> bool:
    return any(kw in query for kw in TECH_KEYWORDS)


def _filter_tech_if_irrelevant(query: str, search_results):
    """如果问题与技术/工作无关，过滤掉编程项目类 RAG 结果"""
    if _has_tech_intent(query):
        return search_results
    filtered = [r for r in search_results.results if r.label not in TECH_LABELS]
    search_results.results = filtered
    return search_results


# 正经模式的触发关键词
PROFESSIONAL_KEYWORDS = [
    "请问", "您", "能否", "介绍一下", "面试", "评估", "优势",
    "劣势", "缺点", "职业规划", "未来目标", "失败", "怎么看待",
    "期望薪资", "离职原因", "入职", "HR", "招聘", "简历",
    "项目经验", "团队合作", "领导力", "自我评价",
]


def _detect_mode(query: str, history: list[dict] | None) -> str:
    """
    从对话中检测应该用哪种人格模式

    Returns:
        "professional" | "casual"  — 模式标识
    """
    # 检查当前问题和最近历史
    texts = [query.lower()]
    if history:
        for m in history[-4:]:  # 最近 4 条
            texts.append(m.get("content", "").lower())

    all_text = " ".join(texts)

    # 命中了正经关键词 → 正经模式
    professional_score = sum(1 for kw in PROFESSIONAL_KEYWORDS if kw.lower() in all_text)

    if professional_score >= 2:
        return "professional"

    return "casual"

# 越界问题的拒绝模板
BOUNDARY_RESPONSE = (
    "抱歉，这个问题涉及个人隐私，我不能回答。"
    "我是{owner}的数字分身，只分享性格、爱好和经历相关的信息。"
    "如果你想联系{owner}本人，请通过其他渠道。"
).format(owner=OWNER_NAME)


class AgentOrchestrator:
    """
    数字分身对话编排器

    用法:
        orchestrator = AgentOrchestrator(searcher)
        async for token in orchestrator.stream("你喜欢什么音乐？"):
            yield token  # SSE event
    """

    def __init__(self, searcher: MemorySearcher) -> None:
        self.searcher = searcher
        self._llm_client: AsyncOpenAI | None = None

    @property
    def llm_available(self) -> bool:
        """检查 LLM 是否可用"""
        if settings.llm_provider == "deepseek":
            return bool(settings.deepseek_api_key)
        return bool(settings.openai_api_key)

    @property
    def llm_client(self) -> AsyncOpenAI:
        """获取 LLM 客户端 — 自动适配 provider 的 base_url"""
        if self._llm_client is None:
            if settings.llm_provider == "deepseek":
                if not settings.deepseek_api_key:
                    raise RuntimeError("DEEPSEEK_API_KEY 未设置")
                self._llm_client = AsyncOpenAI(
                    api_key=settings.deepseek_api_key,
                    base_url="https://api.deepseek.com",
                )
            else:
                if not settings.openai_api_key:
                    raise RuntimeError("OPENAI_API_KEY 未设置")
                self._llm_client = AsyncOpenAI(api_key=settings.openai_api_key)
        return self._llm_client

    async def stream(
        self,
        query: str,
        history: list[dict] | None = None,
    ) -> AsyncIterator[str]:
        """
        流式处理用户问题

        Yields:
            JSON 字符串，格式 {"token": "..."} 或 {"sources": [...]}
        """
        # 1. 意图分类
        intent = classify_intent(query)

        # 2. 越界拒绝
        if intent == "boundary":
            for char in BOUNDARY_RESPONSE:
                yield json.dumps({"token": char}, ensure_ascii=False)
                await asyncio.sleep(0.015)
            return

        # 3. RAG 检索
        search_results = await self.searcher.search(
            query, threshold=settings.retrieval_threshold
        )

        # 3.5 非技术问题过滤编程内容
        search_results = _filter_tech_if_irrelevant(query, search_results)
        persona_context = search_results.context_text

        # 3.6 身份感知 — 检测对方角色，切换正经/真实模式
        mode_hint = _detect_mode(query, history)

        # 4. 组装 prompt（注入模式提示）
        messages = build_messages(
            persona_context=persona_context,
            user_query=query,
            history=history,
            mode_hint=mode_hint,
        )

        # 5. 生成回答 — LLM 优先，无 API Key 时降级为 RAG 直出
        if self.llm_available:
            async for token in self._llm_stream(messages):
                yield token
        else:
            async for token in self._demo_response(search_results):
                yield token

    async def _llm_stream(self, messages: list[dict]) -> AsyncIterator[str]:
        """LLM 流式生成"""
        model = (
            settings.deepseek_model
            if settings.llm_provider == "deepseek"
            else settings.openai_model
        )
        try:
            stream = await self.llm_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                stream=True,
            )
            async for chunk in stream:
                delta = chunk.choices[0].delta
                if delta.content:
                    yield json.dumps({"token": delta.content}, ensure_ascii=False)
        except Exception as e:
            error_msg = f"（AI 服务暂时不可用：{e}）"
            for char in error_msg:
                yield json.dumps({"token": char}, ensure_ascii=False)
                await asyncio.sleep(0.015)

    async def _demo_response(self, search_results) -> AsyncIterator[str]:
        """
        演示模式 — 无 LLM 时，将 RAG 检索结果格式化为自然回答。
        证明 RAG 管道已完全打通，接入 API Key 后即可切换为 LLM 生成。
        """
        from app.retrieval.searcher import SearchResults

        if not search_results.results:
            msg = "抱歉，我在已有数据中没有找到与这个问题相关的信息。你可以直接问本人。"
            for char in msg:
                yield json.dumps({"token": char}, ensure_ascii=False)
                await asyncio.sleep(0.02)
            return

        top = search_results.results[0]
        rest = search_results.results[1:3]

        # 用检索结果拼一段自然回答
        lines = [
            f"根据我的数据，最相关的记忆是「{top.source_type}」中的「{top.label}」（匹配度 {top.similarity:.0%}）。",
            "",
            f"{top.content[:200]}",
            "",
        ]
        if rest:
            lines.append("其他相关条目：")
            for r in rest:
                lines.append(f"  · [{r.source_type}] {r.label}（{r.similarity:.0%}）")
        lines.append("")
        lines.append("---")
        lines.append("💡 这是 RAG 直出模式。接入 OpenAI API Key 后，这里会是 AI 生成的个性化回答。")

        for char in "\n".join(lines):
            yield json.dumps({"token": char}, ensure_ascii=False)
            await asyncio.sleep(0.01)
        sources = [
            {
                "label": r.label,
                "content": r.content[:120],
                "source_type": r.source_type,
                "similarity": r.similarity,
            }
            for r in search_results.results
        ]
        yield json.dumps({"sources": sources}, ensure_ascii=False)
