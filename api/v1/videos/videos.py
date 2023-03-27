from typing import Callable

from fastapi import APIRouter, Depends

from app.controllers import VideoController
from app.models.user import User, UserPermission
from app.schemas.extras.token import Token
from app.schemas.requests.users import LoginUserRequest, RegisterUserRequest
from app.schemas.responses.users import UserResponse
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired
from core.fastapi.dependencies.current_user import get_current_user
from core.fastapi.dependencies.permissions import Permissions
from app.schemas.responses.video_data import VideoResponse

video_router = APIRouter()


# @video_router.get("/{video_name}", dependencies=[Depends(AuthenticationRequired)])
@video_router.get("/{video_name}")
async def get_videos(
    video_name: str,
    controller: VideoController = Depends(Factory().get_video_controller),
) -> VideoResponse:
    videos = await controller.get_by_video_name(video_name)
    return videos
