from fastapi import APIRouter

from .videos import video_router

videos_router = APIRouter()
videos_router.include_router(video_router, tags=["Videos"])

__all__ = ["videos_router"]
