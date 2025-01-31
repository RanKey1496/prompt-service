from fastapi import HTTPException
from sqlmodel import Session, select
from models.video_model import Video, VideoUpdate

def get_videos(session: Session, offset: int = 0, limit: int = 100) -> list[Video]:
    videos = session.exec(select(Video).offset(offset).limit(limit)).all()
    return videos

def get_video(session: Session, id: int) -> Video:
    video = session.exec(select(Video).where(Video.id == id)).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

def create_video(video: Video, session: Session) -> Video:
    session.add(video)
    session.commit()
    session.refresh(video)
    return video

def update_video(id: str, video: VideoUpdate, session: Session) -> Video:
    db_video = session.get(Video, id)
    
    if not db_video:
        raise HTTPException(status_code=404, detail='No se ha encontrado el video')
    
    video_data = video.model_dump(exclude_unset=True)
    db_video.sqlmodel_update(video_data)
    session.add(db_video)
    session.commit()
    session.refresh(db_video)
    return db_video