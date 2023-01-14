from sqlalchemy.ext.asyncio import AsyncSession

from src.accessors import BaseAccessor


class ServiceMixin:
    def __init__(self, session: AsyncSession):
        self.session = session
