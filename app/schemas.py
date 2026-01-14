from pydantic import BaseModel, Field, validator, constr
from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum


class StatusEnum(str, Enum):
    NEW = "new"
    TRANSCODED = "transcoded"
    RECOGNIZED = "recognized"


class VideoBase(BaseModel):
    video_path: constr(min_length=1)
    start_time: datetime
    duration: timedelta
    camera_number: int = Field(gt=0)
    location: constr(min_length=1)

    @validator('duration')
    def validate_duration(cls, v):
        if v <= timedelta(seconds=0):
            raise ValueError('Duration must be positive')
        return v


class VideoCreate(VideoBase):
    pass


class VideoUpdateStatus(BaseModel):
    status: StatusEnum


class VideoResponse(VideoBase):
    id: int
    status: StatusEnum
    created_at: datetime

    class Config:
        from_attributes = True


class VideoListResponse(BaseModel):
    videos: List[VideoResponse]
    total: int


class VideoFilters(BaseModel):
    status: Optional[List[StatusEnum]] = None
    camera_number: Optional[List[int]] = None
    location: Optional[List[str]] = None
    start_time_from: Optional[datetime] = None