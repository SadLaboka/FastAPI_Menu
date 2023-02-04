from celery import Celery
from src.accessors import MenuAccessor, MenuCacheAccessor
from src.core import config


class ServiceMixin:
    def __init__(self, accessor: MenuAccessor, cache_accessor: MenuCacheAccessor):
        self.accessor = accessor
        self.cache_accessor = cache_accessor
        self.celery_app = Celery("tasks", broker=config.RABBITMQ_URL, backend="rpc://")
