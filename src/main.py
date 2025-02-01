from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import check_and_reconnect
from routers import video
from routers import dialog
from routers import media
from config import get_nats_url
from services.nat_service import connect_to_nats, subscribe_to_job_video_result

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(video.router)
app.include_router(dialog.router)
app.include_router(media.router)

@app.on_event("startup")
async def on_startup():
    print("Connecting to NATs...")
    await connect_to_nats(get_nats_url())
    print("Connection successfully to NATs.")
    await subscribe_to_job_video_result()
    
@app.get("/health")
def health():
    check_and_reconnect()
    return { "ready": True }