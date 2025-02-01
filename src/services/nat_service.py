import asyncio
from nats.aio.client import Client as NATS

nc = NATS()

async def connect_to_nats(url):
    await nc.connect(servers=[url])
    
async def publish(topic, data):
    await nc.publish(topic, data)
    
async def subscribe(topic, callback):
    await nc.subscribe(topic, cb=callback)
    
async def publish_jobs_created(id, audio, media):
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
        publish('job.video.created', { 'id': id, 'audio_path': audio, 'media_path': media })