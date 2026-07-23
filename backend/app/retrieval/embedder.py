"""
Embedding 服务 — BGE 模型 查询/文档 不对称编码

BGE (BAAI General Embedding) 模型在训练时采用非对称策略：
- 文档（document / passage）：直接编码原文，不加前缀
- 查询（query）：编码前需要加前缀 "Represent this sentence for searching relevant passages: "

这模拟了训练时的数据分布差异：查询是短的、目标导向的；
文档是长的、信息密集的。如果查询不加前缀，检索效果会显著下降。

参考：https://huggingface.co/BAAI/bge-small-zh-v1.5
"""
from sentence_transformers import SentenceTransformer

from app.core.config import settings

# BGE 模型要求的查询前缀 — 训练时就用的这个
BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


class EmbeddingService:
    """
    BGE Embedding 服务 — 单例模式

    用法:
        svc = EmbeddingService()
        doc_vecs = svc.embed_documents(["外向性: 独处时恢复能量...", ...])
        query_vec = svc.embed_query("你的性格偏内向还是外向？")
    """

    _instance: "EmbeddingService | None" = None

    def __new__(cls) -> "EmbeddingService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True

        model_name = settings.embedding_model
        print(f"[EmbeddingService] Loading {model_name} ...")
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
        print(f"[EmbeddingService] Ready — dim={self.dim}")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """
        编码文档（用于存储到数据库）
        BGE 文档端：不加前缀，直接编码原文
        """
        if not texts:
            return []
        # normalize_embeddings=True → L2 归一化，点积 = 余弦相似度
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]:
        """
        编码查询（用于检索）
        BGE 查询端：必须加前缀！
        """
        prefixed = BGE_QUERY_PREFIX + query
        embedding = self.model.encode(
            [prefixed],
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return embedding[0].tolist()

    def embed_query_batch(self, queries: list[str]) -> list[list[float]]:
        """批量编码查询（每条都会加前缀）"""
        if not queries:
            return []
        prefixed = [BGE_QUERY_PREFIX + q for q in queries]
        embeddings = self.model.encode(
            prefixed,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return embeddings.tolist()
