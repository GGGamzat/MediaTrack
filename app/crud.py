from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from datetime import datetime
from app import models, schemas


def create_video(db: Session, video: schemas.VideoCreate) -> models.Video:
    db_video = models.Video(
        video_path=video.video_path,
        start_time=video.start_time,
        duration=video.duration,
        camera_number=video.camera_number,
        location=video.location,
        status=schemas.StatusEnum.NEW
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def get_video(db: Session, video_id: int) -> Optional[models.Video]:
    return db.query(models.Video).filter(models.Video.id == video_id).first()


def get_videos_with_filters(
        db: Session,
        filters: schemas.VideoFilters,
        skip: int = 0,
        limit: int = 100
) -> List[models.Video]:
    query = db.query(models.Video)

    if filters.status:
        query = query.filter(models.Video.status.in_(filters.status))

    if filters.camera_number:
        query = query.filter(models.Video.camera_number.in_(filters.camera_number))

    if filters.location:
        query = query.filter(models.Video.location.in_(filters.location))

    if filters.start_time_from:
        query = query.filter(models.Video.start_time >= filters.start_time_from)

    query = query.order_by(models.Video.created_at.desc())

    total = query.count()
    videos = query.offset(skip).limit(limit).all()

    return videos, total


def update_video_status(db: Session, video_id: int, status: schemas.StatusEnum) -> Optional[models.Video]:
    db_video = get_video(db, video_id)
    if db_video:
        db_video.status = status
        db.commit()
        db.refresh(db_video)
    return db_video