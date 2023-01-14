from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.accessors import BaseAccessor
from src.models import MenuModel


class MenuAccessor(BaseAccessor):
    async def create_menu(self, title: str, description: str) -> MenuModel:
        menu = MenuModel(title=title, description=description)
        self.session.add(menu)
        await self.session.flush()
        new_menu = await self.get_menu_by_id(menu.id)
        # print(new_menu.id, '---', new_menu.title, '---', new_menu.description, '---', new_menu.submenus, '---', '---')
        # for submenu in new_menu.submenus:
        #     print('+++')
        #     print(submenu.dishes)
        #     print('+++')
        return new_menu

    async def get_menu_by_id(self, id_) -> Optional[MenuModel]:
        menu = (await self.session.scalars(
            select(MenuModel)
            .where(MenuModel.id == id_)
            .options(joinedload(MenuModel.submenus)))
        ).first()
        return menu if menu else None
