"""
FastAPI 入口 — AI 推理层
负责：对话接口、内存 RAG 检索、Agent 编排、LLM 调用
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import chat, health
from app.core.config import settings

app = FastAPI(
    title="Digital Clone API",
    description="数字分身 AI 推理层 — 内存 RAG + 多 Agent 编排",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
