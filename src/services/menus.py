from typing import List, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.accessors import MenuAccessor
from src.api.v1.schemas import (MenuCreate, MenuUpdate, SubMenuCreate,
                                SubMenuUpdate)
from src.db import get_session
from src.models import MenuModel, SubMenuModel
from src.services.mixins import ServiceMixin


class MenuService(ServiceMixin):
    async def create_menu(self, menu: MenuCreate) -> dict:
        """Creates a new menu."""
        async with self.session as db_session:
            async with db_session.begin():
                menu_accessor = MenuAccessor(db_session)
                new_menu = await menu_accessor.create_menu(title=menu.title, description=menu.description)

        answer = await self.make_menu_answer(new_menu)
        return answer

    async def delete_menu(self, menu_id: str) -> bool:
        """Deletes menu by given id."""
        async with self.session as db_session:
            async with db_session.begin():
                menu_accessor = MenuAccessor(db_session)
                result = await menu_accessor.delete_menu_by_id(id_=menu_id)

        return result

    async def get_menu(self, menu_id: str) -> Optional[dict]:
        """Gets a menu for a given id."""
        async with self.session as db_session:
            async with db_session.begin():
                menu_accessor = MenuAccessor(db_session)
                menu = await menu_accessor.get_menu_by_id(id_=menu_id)
        if menu:
            answer = await self.make_menu_answer(menu)
            return answer

    async def get_menu_list(self) -> List[dict]:
        """Gets a menu list."""
        async with self.session as db_session:
            async with db_session.begin():
                menu_accessor = MenuAccessor(db_session)
                menus = await menu_accessor.get_menus()

        return [await self.make_menu_answer(menu) for menu in menus]

    async def update_menu(self, menu_id: str, new_data: MenuUpdate) -> Optional[dict]:
        """Updates a menu for a given id."""
        async with self.session as db_session:
            async with db_session.begin():
                menu_accessor = MenuAccessor(db_session)
                menu = await menu_accessor.update_menu(
                    id_=menu_id, title=new_data.title, description=new_data.description)
        if menu:
            answer = await self.make_menu_answer(menu)
            return answer

    async def create_submenu(self, menu_id: str, submenu: SubMenuCreate) -> dict:
        """Creates a new submenu."""
        async with self.session as db_session:
            async with db_session.begin():
                menu_accessor = MenuAccessor(db_session)
                submenu = await menu_accessor.create_submenu(
                    menu_id=menu_id, title=submenu.title, description=submenu.description)

        answer = await self.make_submenu_answer(submenu)
        return answer

    async def delete_submenu(self, submenu_id: str) -> bool:
        """Deletes submenu by given id."""
        async with self.session as db_session:
            async with db_session.begin():
                menu_accessor = MenuAccessor(db_session)
                result = await menu_accessor.delete_submenu_by_id(id_=submenu_id)

        return result

    async def get_submenu(self, submenu_id: str) -> Optional[dict]:
        """Gets a submenu for a given id."""
        async with self.session as db_session:
            async with db_session.begin():
                menu_accessor = MenuAccessor(db_session)
                submenu = await menu_accessor.get_submenu_by_id(id_=submenu_id)
        if submenu:
            answer = await self.make_submenu_answer(submenu)
            return answer

    async def get_submenus(self, menu_id: str) -> List[dict]:
        """Gets a submenu list."""
        async with self.session as db_session:
            async with db_session.begin():
                menu_accessor = MenuAccessor(db_session)
                submenus = await menu_accessor.get_submenus(menu_id=menu_id)

        return [await self.make_submenu_answer(submenu) for submenu in submenus]

    async def update_submenu(self, submenu_id: str, new_data: SubMenuUpdate) -> Optional[dict]:
        """Updates a new submenu."""
        async with self.session as db_session:
            async with db_session.begin():
                menu_accessor = MenuAccessor(db_session)
                submenu = await menu_accessor.update_submenu(
                    id_=submenu_id, title=new_data.title, description=new_data.description)
        if submenu:
            answer = await self.make_submenu_answer(submenu)
            return answer

    @staticmethod
    async def make_menu_answer(menu: MenuModel) -> dict:
        """Converts an object to the desired format"""
        answer = {
            'id': menu.id,
            'title': menu.title,
            'description': menu.description,
            'submenus_count': len(menu.submenus),
            'dishes_count': sum([len(submenu.dishes) for submenu in menu.submenus]) if menu.submenus else 0,
        }
        return answer

    @staticmethod
    async def make_submenu_answer(submenu: SubMenuModel) -> dict:
        """Converts an object to the desired format"""
        answer = {
            'id': submenu.id,
            'title': submenu.title,
            'description': submenu.description,
            'dishes_count': len(submenu.dishes)
        }
        return answer


async def get_menu_service(
        session: AsyncSession = Depends(get_session),
) -> MenuService:
    return MenuService(session=session)
