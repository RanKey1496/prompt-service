from fastapi import APIRouter
from services.s3 import generated_presigned_url
from models.requests.media import PresignedURL

router = APIRouter()

@router.post("/s3/presigned_url")
def get_pressigned_url(data: PresignedURL) -> dict:
    return generated_presigned_url(data.id, data.type, data.filename, data.content_type)