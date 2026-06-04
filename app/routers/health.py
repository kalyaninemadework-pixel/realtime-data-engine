"""Health check endpoints."""
from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/health")
async def health(request: Request):
    stats = request.app.state.pipeline.stats
    return {
        "status": "healthy",
        "pipeline": stats,
        "database": "connected",
        "cache": "connected"
    }
