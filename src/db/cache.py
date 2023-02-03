from abc import ABC, abstractmethod

from aioredis.client import Redis

from src.core import config


class AbstractCache(ABC):
    def __init__(self, cache_instance):
        self.cache: dict | Redis = cache_instance

    @abstractmethod
    async def get(self, key: str):
        pass

    @abstractmethod
    async def set(
        self,
        key: str,
        value: bytes | str,
        expire: int = config.CACHE_EXPIRE_IN_SECONDS,
    ):
        pass

    @abstractmethod
    async def remove(self, key: str):
        pass

    @abstractmethod
    async def close(self):
        pass


class RedisCache(AbstractCache):
    async def get(self, key: str):
        item = await self.cache.get(key)  # type: ignore
        return item

    async def set(
        self,
        key: str,
        value: bytes | str,
        expire: int = config.CACHE_EXPIRE_IN_SECONDS,
    ):
        await self.cache.set(name=key, value=value, ex=expire)  # type: ignore

    async def remove(self, key: str):
        await self.cache.delete(key)  # type: ignore

    async def close(self):
        await self.cache.close()


cache: AbstractCache | None = None


async def get_cache() -> AbstractCache:
    """Gets the cache instance for dependency injection."""
    return RedisCache(cache)
