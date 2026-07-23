"""
应用配置 — 集中管理环境变量与常量
"""
import os
from pathlib import Path
from typing import Optional


def _load_dotenv():
    """加载 backend/.env 文件到环境变量"""
    # 向上查找 backend/.env
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    if env_path.exists():
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    if key.strip() not in os.environ:
                        os.environ[key.strip()] = value.strip()


_load_dotenv()


class Settings:
    """从环境变量加载配置，dotenv 在启动脚本中预加载"""

    # 服务
    app_name: str = "Digital Clone API"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    cors_origins: list[str] = os.getenv(
        "CORS_ORIGINS", "http://localhost:3000"
    ).split(",")

    # Embedding
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5"
    )

    # LLM
    llm_provider: str = os.getenv("LLM_PROVIDER", "deepseek")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    deepseek_api_key: Optional[str] = os.getenv("DEEPSEEK_API_KEY")
    deepseek_model: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    # 检索
    retrieval_top_k: int = int(os.getenv("RETRIEVAL_TOP_K", "5"))
    retrieval_threshold: float = float(os.getenv("RETRIEVAL_THRESHOLD", "0.38"))


settings = Settings()
