from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app import crud, models, schemas
from app.database import get_db, engine
import logging

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MediaTrack", description="REST API для работы с базой данных видео")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/videos", response_model=schemas.VideoResponse, status_code=status.HTTP_201_CREATED)
def create_video_endpoint(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_video(db=db, video=video)
    except Exception as e:
        logger.error(f"Error creating video: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/videos", response_model=schemas.VideoListResponse)
def get_videos_endpoint(
        status: Optional[List[schemas.StatusEnum]] = Query(None),
        camera_number: Optional[List[int]] = Query(None),
        location: Optional[List[str]] = Query(None),
        start_time_from: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    try:
        filters = schemas.VideoFilters(
            status=status,
            camera_number=camera_number,
            location=location,
            start_time_from=start_time_from
        )

        videos, total = crud.get_videos_with_filters(
            db=db,
            filters=filters,
            skip=skip,
            limit=limit
        )

        return schemas.VideoListResponse(videos=videos, total=total)
    except Exception as e:
        logger.error(f"Error getting videos: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/videos/{video_id}", response_model=schemas.VideoResponse)
def get_video_endpoint(video_id: int, db: Session = Depends(get_db)):
    video = crud.get_video(db=db, video_id=video_id)
    if video is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Video with id {video_id} not found")
    return video


@app.patch("/videos/{video_id}/status", response_model=schemas.VideoResponse)
def update_video_status_endpoint(
        video_id: int,
        status_update: schemas.VideoUpdateStatus,
        db: Session = Depends(get_db)
):
    video = crud.update_video_status(
        db=db,
        video_id=video_id,
        status=status_update.status
    )
    if video is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Video with id {video_id} not found"
        )
    return video


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)