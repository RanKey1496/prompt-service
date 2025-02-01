import asyncio
import json
from typing import Annotated
from fastapi import Depends, APIRouter, Query, Request
from fastapi.responses import StreamingResponse
from sqlmodel import Session
from db import get_session
from models.video_model import Video, VideoUpdate
from services.video_service import get_videos, get_video, create_video, update_video
from services.nat_service import publish_job_created, publish_job_result, event_queue
from services.s3_service import generate_result_url

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
async def patch_video(id: str, video: VideoUpdate, session: SessionDep):
    video = update_video(id, video, session)
    await publish_job_created(id, video.audio_path, video.media_path)
    await publish_job_result(id)
    return video

@router.get("/videos/{id}/result")
async def get_result(id: str, session: SessionDep):
    video = get_video(session, id)
    return generate_result_url(video.video_path)

@router.get("/videos/{id}/status")
async def check_video_status(id: int, request: Request):
    if id not in event_queue:
        event_queue[id] = asyncio.Queue()
    
    async def event_generator():
        try:
            while True:
                data = await event_queue[id].get()
                yield f"data: {json.dumps(data)}\n\n"
                
                if await request.is_disconnected():
                    break
        except asyncio.CancelledError:
            pass
        finally:
            if id in event_queue:
                del event_queue[id]
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")