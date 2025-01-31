from pydantic import BaseModel

class PresignedURL(BaseModel):
    id: str
    type: str
    filename: str
    content_type: str