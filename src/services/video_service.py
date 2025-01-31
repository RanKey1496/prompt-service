from fastapi import HTTPException
from sqlmodel import Session, select
from models.video_model import Video

def get_videos(session: Session, offset: int = 0, limit: int = 100) -> list[Video]:
    videos = session.exec(select(Video).offset(offset).limit(limit)).all()
    return videos

def get_video(session: Session, id: int) -> Video:
    video = session.exec(select(Video).where(Video.id == id)).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video