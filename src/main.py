from fastapi import FastAPI
from routers import video
from routers import dialog

app = FastAPI()

app.include_router(video.router)
app.include_router(dialog.router)

@app.on_event("startup")
def on_startup():
    print("on_startup")