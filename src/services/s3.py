import os
import boto3
from fastapi import HTTPException
from config import get_s3_region, get_s3_key, get_s3_secret, get_s3_bucket

s3_client = boto3.client(
            service_name='s3',
            region_name=get_s3_region(),
            aws_access_key_id=get_s3_key(),
            aws_secret_access_key=get_s3_secret()
        )

def generated_presigned_url(id: str, type: str, filename: str, content_type: str):
    try:
        if type == 'audio':
            key = os.path.join('audio', id, filename)
        elif type == 'media':
            key = os.path.join('video', id, filename)
        else:
            key = os.path.join('media', id, filename)
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': get_s3_bucket(),
                'Key': key,
                'ContentType': content_type
            },
            ExpiresIn=3600
        )
        return { 'data': presigned_url}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail='No se ha podido generar la URL')