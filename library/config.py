from os.path import join
from pathlib import Path
from os import getenv
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
ENV_PATH = join(BASE_DIR, '.env')
load_dotenv(ENV_PATH)

# Takes database configuration from environment variables
class DBConfig:
    DB_USER = getenv("DB_USER")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_NAME = getenv("DB_NAME")
    DB_HOST = getenv("DB_HOST")
    DB_PORT = getenv("DB_PORT")
    DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"



