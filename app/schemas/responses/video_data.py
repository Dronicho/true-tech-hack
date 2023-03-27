from pydantic import UUID4, BaseModel, Field
from typing import List


class VideoItem(BaseModel):
    startTime: int = Field(..., example="1", title="Начало фильтра в секундах")
    endTime: int = Field(..., example="5", title="Конец фильтра в секундах")
    actions: List[str] = Field(..., example=['blur'], title="Список фильтров")


class VideoResponse(BaseModel):
    name: str = Field(..., example="output")
    data: List[VideoItem] = Field(...)
