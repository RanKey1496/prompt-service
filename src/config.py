import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_db_url():
    return os.environ.get("DATABASE_URL")

def get_nats_url():
    return os.environ.get("NATS_URL")

def get_s3_region():
    return os.environ.get("S3_REGION")

def get_s3_bucket():
    return os.environ.get("S3_BUCKET")

def get_s3_key():
    return os.environ.get("S3_KEY")

def get_s3_secret():
    return os.environ.get("S3_SECRET")