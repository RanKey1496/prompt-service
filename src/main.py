from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import video
from routers import dialog

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(video.router)
app.include_router(dialog.router)

@app.on_event("startup")
def on_startup():
    print("on_startup")