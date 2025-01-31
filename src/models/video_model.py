from typing import List
from datetime import datetime
from sqlmodel import SQLModel, Field, ARRAY, Column, String

class Video(SQLModel, table=True):
    __tablename__ = "videos"
    
    id: int = Field(primary_key=True, index=True)
    title: str = Field(nullable=False)
    prompt: str = Field(nullable=False)
    audio_path: str = Field(nullable=True)
    media_path: List[str] = Field(sa_column = Column(ARRAY(String)), default=None)
    video_path: str = Field(nullable=True)
    created_at: datetime = Field(default=datetime.now())