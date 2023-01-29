from src.accessors import MenuAccessor, MenuCacheAccessor


class ServiceMixin:
    def __init__(self, accessor: MenuAccessor, cache_accessor: MenuCacheAccessor):
        self.accessor = accessor
        self.cache_accessor = cache_accessor
