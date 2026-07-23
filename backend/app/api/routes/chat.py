"""
对话接口 — 流式 SSE 响应
POST /api/chat  →  SSE 流返回 AI 回答 + 检索来源
"""
import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.models.persona import ChatRequest
from app.retrieval.embedder import EmbeddingService
from app.retrieval.memory_searcher import MemorySearcher
from app.agents.orchestrator import AgentOrchestrator

router = APIRouter()

# 模块级单例 — 启动时加载 BGE 模型 + YAML 数据
_embedder: EmbeddingService | None = None
_searcher: MemorySearcher | None = None


def get_orchestrator() -> AgentOrchestrator:
    global _embedder, _searcher
    if _embedder is None:
        _embedder = EmbeddingService()
    if _searcher is None:
        _searcher = MemorySearcher(_embedder)
    return AgentOrchestrator(_searcher)


@router.post("/chat")
async def chat(
    request: ChatRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
):
    """对话端点 — Server-Sent Events 流式响应"""

    history = [{"role": m.role, "content": m.content} for m in request.history]

    async def generate():
        async for event in orchestrator.stream(request.query, history):
            yield f"data: {event}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
