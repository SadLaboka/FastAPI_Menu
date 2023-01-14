from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.accessors import MenuAccessor
from src.api.v1.schemas import MenuCreate
from src.db import get_session
from src.services.mixins import ServiceMixin


class MenuService(ServiceMixin):
    async def create_menu(self, menu: MenuCreate) -> dict:
        async with self.session as db_session:
            async with db_session.begin():
                menu_accessor = MenuAccessor(db_session)
                new_menu = await menu_accessor.create_menu(title=menu.title, description=menu.description)

        answer = {
            'id': new_menu.id,
            'title': new_menu.title,
            'description': new_menu.description,
            'submenus_count': len(new_menu.submenus),
            'dishes_count': sum([len(submenu.dishes) for submenu in new_menu.submenus]) if new_menu.submenus else 0,
        }
        return answer


async def get_menu_service(
        session: AsyncSession = Depends(get_session),
) -> MenuService:

    return MenuService(session=session)
