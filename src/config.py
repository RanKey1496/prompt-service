import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_db_url():
    return os.environ.get("DATABASE_URL")