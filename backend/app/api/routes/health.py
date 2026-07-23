"""健康检查路由"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Kubernetes/docker-compose 健康检查端点"""
    return {"status": "ok", "service": "digital-clone-api"}
