import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FastAPI-Ylab")
VERSION: str = "1.0.0"

# Postgres Settings
POSTGRES_HOST: str = os.getenv("DBHOST", "localhost")
POSTGRES_PORT: int = int(os.getenv("DBPORT", 5432))
POSTGRES_DB: str = os.getenv("DBNAME", "postgres")
POSTGRES_USER: str = os.getenv("DBUSER", "postgres")
POSTGRES_PASSWORD: str = os.getenv("DBPASSWORD", "postgres")

DATABASE_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}" \
                    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent
