from collections.abc import Generator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core import config

db_base = declarative_base()

engine = create_async_engine(
    config.DATABASE_URL, future=True, echo=True,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> Generator:
    """Gets the db-session for dependency injection."""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
