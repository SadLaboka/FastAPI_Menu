import asyncio
from collections.abc import Generator
from typing import Any

import asyncpg
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from main import app
from src.core import config
from src.db import get_session
from src.db.cache import AbstractCache, get_cache


class TestCache(AbstractCache):

    async def get(self, key: str):
        return self.cache.get(key)

    async def set(
            self,
            key: str,
            value: bytes | str,
            expire: int = config.CACHE_EXPIRE_IN_SECONDS,
    ):
        self.cache[key] = value

    async def remove(self, key: str):
        try:
            self.cache.pop(key)
        except KeyError:
            pass

    async def close(self):
        pass


test_engine = create_async_engine(config.TEST_DATABASE_URL, future=True, echo=True)

# create session for the interaction with database
test_async_session = sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)

CLEAN_TABLES = [
    "menu",
    "submenu",
    "dish",
]


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
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(text(f"""TRUNCATE TABLE {table_for_cleaning} CASCADE;"""))


async def _get_test_db():
    try:
        yield test_async_session()
    finally:
        pass


async def _get_test_cache():
    return TestCache(dict())


@pytest.fixture
async def client() -> Generator[AsyncClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """
    app.dependency_overrides[get_session] = _get_test_db
    app.dependency_overrides[get_cache] = _get_test_cache
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool("".join(config.TEST_DATABASE_URL.split("+asyncpg")))
    yield pool
    await pool.close()


@pytest.fixture
async def create_menu_in_database(asyncpg_pool):
    async def create_menu_in_database(id_: str, title: str, description: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO menu VALUES ($1, $2, $3)""",
                id_, title, description,
            )

    return create_menu_in_database


@pytest.fixture
async def create_submenu_in_database(asyncpg_pool):
    async def create_submenu_in_database(id_: str, title: str, description: str, menu_id: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO submenu VALUES ($1, $2, $3, $4)""",
                id_, title, description, menu_id,
            )

    return create_submenu_in_database


@pytest.fixture
async def create_dish_in_database(asyncpg_pool):
    async def create_dish_in_database(id_: str, title: str, description: str, price: float, submenu_id: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO dish VALUES ($1, $2, $3, $4, $5)""",
                id_, title, description, price, submenu_id,
            )

    return create_dish_in_database


@pytest.fixture
async def delete_submenu_from_database(asyncpg_pool):
    async def delete_submenu_from_database(id_: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute("""DELETE FROM submenu WHERE id = $1;""", id_)

    return delete_submenu_from_database


@pytest.fixture
async def delete_menu_from_database(asyncpg_pool):
    async def delete_menu_from_database(id_: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute("""DELETE FROM menu WHERE id = $1;""", id_)

    return delete_menu_from_database


@pytest.fixture
def dish_data():
    return {
        "id_": "4468bbfd-e02e-4936-9e27-402520dcecf2",
        "submenu_id": "4468bbfd-e02e-4936-9e26-402520dcecf2",
        "title": "Test dish",
        "price": 14.5,
        "description": "Test dish description",
    }


@pytest.fixture
def submenu_data():
    return {
        "id_": "4468bbfd-e02e-4936-9e26-402520dcecf2",
        "menu_id": "4468bbfd-e02e-4936-9e25-402520dcecf2",
        "title": "Test submenu",
        "description": "Test submenu description",
    }


@pytest.fixture
def menu_data():
    return {
        "id_": "4468bbfd-e02e-4936-9e25-402520dcecf2",
        "title": "Test menu",
        "description": "Test menu description",
    }
