from typing import Annotated
from fastapi import Depends, APIRouter, Query
from sqlmodel import Session
from db import get_session
from models.video_model import Video
from services.video_service import get_videos, get_video

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