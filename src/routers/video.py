from typing import Annotated
from fastapi import Depends, APIRouter, Query
from sqlmodel import Session
from db import get_session
from models.video_model import Video, VideoUpdate
from services.video_service import get_videos, get_video, create_video, update_video
from services.nat_service import publish_jobs_created

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/videos/")
def read_videos(session: SessionDep,
                offset: int = 0,
                limit: Annotated[int, Query(le=100)] = 100) -> list[Video]:
    return get_videos(session, offset, limit)

@router.get("/videos/{video_id}")
def read_video(session: SessionDep,
               video_id: int):
    return get_video(session, video_id)

@router.post("/videos")
def save_video(video: Video, session: SessionDep):
    return create_video(video, session)

@router.patch("/videos/{id}")
def patch_video(id: str, video: VideoUpdate, session: SessionDep):
    video = update_video(id, video, session)
    publish_jobs_created(id, video.audio_path, video.media_path)