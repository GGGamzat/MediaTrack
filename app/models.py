from sqlalchemy import Column, Integer, String, DateTime, Interval
from datetime import datetime, timedelta
from app.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    video_path = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    duration = Column(Interval, nullable=False)
    camera_number = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    status = Column(String, nullable=False, default="new")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Video(id={self.id}, camera={self.camera_number}, status={self.status})>"