from app.repositories import VideoRepository


class VideoController:
    def __init__(self, video_repository: VideoRepository):
        self.repository = video_repository

    async def get_by_video_name(self, video_name):
        return await self.repository.get_by_field("name", video_name)
