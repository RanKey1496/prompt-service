import asyncio
import json
from nats.aio.client import Client as NATS

nc = NATS()
event_queue = {}

async def connect_to_nats(url):
    await nc.connect(servers=[url])
    
async def publish(topic, data):
    await nc.publish(topic, data)
    
async def subscribe_to_job_video_result():
    async def message_handdler(msg):
        subject = msg.subject
        data = json.loads(msg.data.decode())
        print(f"Mensaje recibido en el tema '{subject}': {data}")
        
        video_id = data.get('id')
        if video_id and video_id in event_queue:
            await event_queue[video_id].put(data)
            print(f'Mensaje enviado a la cola con id {video_id}')
    await nc.subscribe('job.video.result', cb=message_handdler)
    print(f"Subscrito al tema: job.video.result")
    
async def publish_job_created(id, audio, media):
    if (not audio and not media):
        #Publicar a tts-service
        #Publicar a media-service
        return
    
    if (not audio and media):
        #Publicar a tts-service
        return
    
    if (audio and not media):
        #Publicar a media-service
        return
    
    if (audio and media):
        print('Publising to job.video.created')
        data = { 'id': id, 'audio_path': audio, 'media_path': media }
        await publish('job.video.created', json.dumps(data).encode())
        
async def publish_job_result(id):
    data = { 'id': id, 'status': 'created' }
    await publish('job.video.result', json.dumps(data).encode())