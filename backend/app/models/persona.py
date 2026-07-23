"""
人格数据模型 — 整个系统的核心数据结构
定义性格维度、兴趣爱好、人生事件的 Schema
同时用于 Pydantic 校验 + ORM 映射 + JSON Schema 生成
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class PersonalityDimension(BaseModel):
    """人格维度：大五人格 / MBTI 等性格测试的结构化结果"""

    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., description="维度名称，如 '外向性'")
    score: float = Field(
        ..., ge=0.0, le=1.0, description="0.0(极低) ~ 1.0(极高)"
    )
    description: str = Field(
        ..., description="对该维度的叙事化描述，供 AI 检索和引用"
    )
    source: Optional[str] = Field(
        None, description="数据来源：MBTI测试 / 自我评估 / 朋友反馈"
    )
    created_at: datetime = Field(default_factory=datetime.now)


class Interest(BaseModel):
    """兴趣爱好 — 多级标签 + 叙事文本"""

    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., description="兴趣名称，如 '阅读'")
    category: str = Field(..., description="分类：文艺 / 运动 / 技术 / 社交 / 其他")
    level: int = Field(default=3, ge=1, le=5, description="热衷程度 1~5")
    keywords: list[str] = Field(
        default_factory=list, description="关联关键词，如 ['科幻', '村上春树']"
    )
    narrative: str = Field(
        default="", description="一段话描述与这个爱好的个人关系"
    )


class LifeEvent(BaseModel):
    """人生关键事件 — 塑造人格的重要经历"""

    id: UUID = Field(default_factory=uuid4)
    date: str = Field(..., description="日期，格式 YYYY-MM 或 YYYY")
    title: str = Field(..., description="事件标题")
    impact: str = Field(..., description="该事件对人格/观念的影响")
    tags: list[str] = Field(default_factory=list, description="标签：职业/自我认知/转折点")


class ChatMessage(BaseModel):
    """对话消息"""

    role: str = Field(..., pattern="^(user|assistant)$")
    content: str = Field(...)


class ChatRequest(BaseModel):
    """对话请求"""

    query: str = Field(..., min_length=1, max_length=2000)
    history: list[ChatMessage] = Field(default_factory=list)


class RetrievedSource(BaseModel):
    """检索到的数据来源记录 — 可观测性的基础"""

    table: str
    name: str
    description: str
    similarity: float


class ChatResponse(BaseModel):
    """对话响应"""

    answer: str
    sources: list[RetrievedSource] = Field(default_factory=list)
