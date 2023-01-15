import asyncio
from typing import Any, Generator

import asyncpg
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from main import app
from src.core import config
from src.db import get_session

test_engine = create_async_engine(config.TEST_DATABASE_URL, future=True, echo=True)

# create session for the interaction with database
test_async_session = sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(config.TEST_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    CLEAN_TABLES = [
        "menu",
        "submenu",
        "dish"
    ]
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(f"""TRUNCATE TABLE {table_for_cleaning} CASCADE;""")


async def _get_test_db():
    try:
        yield test_async_session()
    finally:
        pass


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    app.dependency_overrides[get_session] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool("".join(config.TEST_DATABASE_URL.split("+asyncpg")))
    yield pool
    await pool.close()


@pytest.fixture
async def create_menu_in_database(asyncpg_pool):

    async def create_menu_in_database(id_: str, title: str, description: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute("""INSERT INTO menu VALUES ($1, $2, $3)""",
                                            id_, title, description)
    return create_menu_in_database
