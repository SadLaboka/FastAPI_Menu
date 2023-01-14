from sqlalchemy.ext.asyncio import AsyncSession


class BaseAccessor:
    def __init__(self, session: AsyncSession):
        self.session = session
