"""
内存检索引擎 — YAML 加载 + numpy 向量检索
20 条数据在内存中完成检索，< 1ms

架构:
  启动时: YAML → 文档列表 → BGE embed_documents → numpy 矩阵
  查询时: embed_query → numpy 矩阵乘法 → 排序 → 过滤 → 返回
"""
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import yaml

from app.core.config import settings
from app.retrieval.embedder import EmbeddingService

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"


@dataclass
class SearchResult:
    """检索结果 — 与旧接口兼容"""

    label: str
    content: str
    source_type: str
    similarity: float


@dataclass
class SearchResults:
    """检索结果集 — 与旧接口兼容"""

    query: str
    results: list[SearchResult] = field(default_factory=list)

    @property
    def context_text(self) -> str:
        if not self.results:
            return "（未找到相关个人信息）"
        parts = [f"[{r.source_type}] {r.label}: {r.content}" for r in self.results]
        return "\n".join(parts)


class MemorySearcher:
    """
    内存语义检索器 — 零外部依赖，纯 numpy

    用法（与 HybridSearcher 接口相同）:
        searcher = MemorySearcher(embedder)
        results = await searcher.search("你喜欢什么音乐？")
    """

    def __init__(self, embedder: EmbeddingService) -> None:
        self.embedder = embedder
        self._documents: list[dict] = []
        self._embeddings: np.ndarray = np.array([])

        # 启动时加载数据
        self._load_all()

    def _load_all(self) -> None:
        """加载所有 YAML 文件并生成文档向量"""
        docs: list[dict] = []
        texts: list[str] = []

        # 人格维度
        dims_path = DATA_DIR / "persona" / "dimensions.yaml"
        if dims_path.exists():
            with open(dims_path, encoding="utf-8") as f:
                dims = yaml.safe_load(f)
            for d in dims.get("personality_dimensions", []):
                text = f"{d['name']}: {d['description']}"
                docs.append({
                    "label": d["name"],
                    "content": d["description"],
                    "source_type": "性格与价值观",
                })
                texts.append(text)

        # 兴趣爱好
        hobbies_path = DATA_DIR / "interests" / "hobbies.yaml"
        if hobbies_path.exists():
            with open(hobbies_path, encoding="utf-8") as f:
                hobbies = yaml.safe_load(f)
            for h in hobbies.get("interests", []):
                text = f"{h['name']}: {h['narrative']}"
                docs.append({
                    "label": h["name"],
                    "content": h["narrative"],
                    "source_type": "兴趣爱好",
                })
                texts.append(text)

        # 人生经历
        timeline_path = DATA_DIR / "timeline" / "events.yaml"
        if timeline_path.exists():
            with open(timeline_path, encoding="utf-8") as f:
                timeline = yaml.safe_load(f)
            for e in timeline.get("events", []):
                text = f"时间: {e['date']} | {e['title']}: {e['impact']}"
                docs.append({
                    "label": e["title"],
                    "content": f"{e['date']}: {e['impact']}",
                    "source_type": "人生经历",
                })
                texts.append(text)

        self._documents = docs

        # 生成文档向量（BGE 文档端，不加查询前缀）
        if texts:
            embeddings = self.embedder.embed_documents(texts)
            self._embeddings = np.array(embeddings, dtype=np.float32)

        print(f"[MemorySearcher] 加载 {len(docs)} 条文档, embedding shape={self._embeddings.shape}")

    async def search(
        self,
        query: str,
        top_k: int | None = None,
        threshold: float | None = None,
    ) -> SearchResults:
        """
        内存向量检索 — numpy 矩阵乘法

        Args:
            query: 用户问题
            top_k: 返回 top N 条
            threshold: 相似度阈值
        """
        top_k = top_k or settings.retrieval_top_k
        threshold = threshold or settings.retrieval_threshold

        if len(self._documents) == 0:
            return SearchResults(query=query)

        # 查询向量（加 BGE 前缀）
        q_vec = np.array(self.embedder.embed_query(query), dtype=np.float32)

        # 矩阵乘法 — 余弦相似度（向量已 L2 归一化，点积 = 余弦相似度）
        scores = np.dot(self._embeddings, q_vec)

        # 按分数降序排序，取 top_k
        indices = np.argsort(scores)[::-1][:top_k]

        results: list[SearchResult] = []
        for idx in indices:
            sim = float(scores[idx])
            if sim < threshold:
                continue
            doc = self._documents[idx]
            results.append(SearchResult(
                label=doc["label"],
                content=doc["content"],
                source_type=doc["source_type"],
                similarity=round(sim, 4),
            ))

        return SearchResults(query=query, results=results)
