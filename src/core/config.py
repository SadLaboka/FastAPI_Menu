import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FastAPI-Ylab")
VERSION: str = "1.0.0"
BASE_URL: str = "http://localhost:8000"

# Postgres Settings
POSTGRES_HOST: str = os.getenv("DBHOST", "localhost")
POSTGRES_PORT: int = int(os.getenv("DBPORT", 5432))
POSTGRES_DB: str = os.getenv("DBNAME", "postgres")
POSTGRES_USER: str = os.getenv("DBUSER", "postgres")
POSTGRES_PASSWORD: str = os.getenv("DBPASSWORD", "postgres")

DATABASE_URL: str = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
# URL for tests
TEST_DB_URL: str = os.getenv("TEST_DB_URL", "test-db")
TEST_DATABASE_URL: str = f"postgresql+asyncpg://test:test@{TEST_DB_URL}:5432/test"

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Redis
REDIS_HOST: str = os.getenv("REDIS_HOST", "redis-cache")
REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
CACHE_EXPIRE_IN_SECONDS: int = int(os.getenv("CACHE_EXPIRE_IN_SECONDS", 600))

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# RabbitMQ
RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASS: str = os.getenv("RABBITMQ_PASS", "mypass")

RABBITMQ_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:5672"
