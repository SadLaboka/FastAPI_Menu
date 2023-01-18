from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

from src.accessors import BaseAccessor
from src.models import DishModel, MenuModel, SubMenuModel


class MenuAccessor(BaseAccessor):
    async def create_menu(self, title: str, description: str) -> MenuModel:
        menu = MenuModel(title=title, description=description)
        async with self.session as db_session:
            async with db_session.begin():
                self.session.add(menu)
                await self.session.flush()
        new_menu = await self.get_menu_by_id(menu.id)
        return new_menu

    async def delete_menu_by_id(self, id_: str) -> bool:
        menu = await self.get_menu_by_id(id_)
        if menu:
            async with self.session as db_session:
                async with db_session.begin():
                    await self.session.delete(menu)
                    await self.session.commit()
            return True
        return False

    async def get_menu_by_id(self, id_: str) -> Optional[MenuModel]:
        async with self.session as db_session:
            async with db_session.begin():
                menu = (await self.session.scalars(
                    select(MenuModel)
                    .where(MenuModel.id == id_)
                    .options(joinedload(MenuModel.submenus).joinedload(SubMenuModel.dishes)))
                        ).first()
        return menu if menu else None

    async def get_menus(self) -> List[MenuModel]:
        async with self.session as db_session:
            async with db_session.begin():
                menus = await self.session.scalars(
                    select(MenuModel)
                    .options(joinedload(MenuModel.submenus).joinedload(SubMenuModel.dishes)))

        return [menu for menu in menus.unique()]

    async def update_menu(self, id_: str, title: str, description: str) -> Optional[MenuModel]:
        async with self.session as db_session:
            async with db_session.begin():
                await self.session.execute(update(MenuModel).where(
                    MenuModel.id == id_
                ).values(
                    title=title,
                    description=description
                ))
        updated_menu = await self.get_menu_by_id(id_)
        return updated_menu

    async def create_submenu(self, menu_id: str, title: str, description: str) -> SubMenuModel:
        submenu = SubMenuModel(title=title, description=description, menu_id=menu_id)
        async with self.session as db_session:
            async with db_session.begin():
                self.session.add(submenu)
        await self.session.flush()
        new_submenu = await self.get_submenu_by_id(submenu.id)
        return new_submenu

    async def get_submenu_by_id(self, id_: str) -> Optional[SubMenuModel]:
        async with self.session as db_session:
            async with db_session.begin():
                submenu = (await self.session.scalars(
                    select(SubMenuModel)
                    .where(SubMenuModel.id == id_)
                    .options(joinedload(SubMenuModel.dishes)))
                           ).first()
        return submenu if submenu else None

    async def get_submenus(self, menu_id: str) -> List[SubMenuModel]:
        async with self.session as db_session:
            async with db_session.begin():
                submenus = await self.session.scalars(
                    select(SubMenuModel)
                    .where(SubMenuModel.menu_id == menu_id)
                    .options(joinedload(SubMenuModel.dishes)))

        return [submenu for submenu in submenus.unique()]

    async def update_submenu(self, id_: str, title: str, description: str) -> Optional[SubMenuModel]:
        async with self.session as db_session:
            async with db_session.begin():
                await self.session.execute(update(SubMenuModel).where(
                    SubMenuModel.id == id_
                ).values(
                    title=title,
                    description=description
                ))
        updated_submenu = await self.get_submenu_by_id(id_)
        return updated_submenu

    async def delete_submenu_by_id(self, id_: str) -> bool:
        submenu = await self.get_submenu_by_id(id_)
        if submenu:
            async with self.session as db_session:
                async with db_session.begin():
                    await self.session.delete(submenu)
                    await self.session.commit()
            return True
        return False

    async def create_dish(self, submenu_id: str, title: str, description: str, price: str) -> DishModel:
        dish = DishModel(submenu_id=submenu_id, title=title, description=description, price=float(price))
        async with self.session as db_session:
            async with db_session.begin():
                self.session.add(dish)
                await self.session.flush()
        return dish

    async def get_dish_by_id(self, dish_id: str) -> Optional[DishModel]:
        async with self.session as db_session:
            async with db_session.begin():
                dish = (await self.session.scalars(
                    select(DishModel)
                    .where(DishModel.id == dish_id))).first()
        return dish if dish else None

    async def get_dishes(self, submenu_id: str) -> List[DishModel]:
        async with self.session as db_session:
            async with db_session.begin():
                dishes = (await self.session.scalars(
                    select(DishModel)
                    .where(DishModel.submenu_id == submenu_id)
                ))
        return [dish for dish in dishes.unique()]

    async def update_dish(self, dish_id: str, title: str, description: str, price: str) -> Optional[DishModel]:
        async with self.session as db_session:
            async with db_session.begin():
                await self.session.execute(update(DishModel).where(
                    DishModel.id == dish_id
                ).values(
                    title=title,
                    description=description,
                    price=float(price)
                ))
        updated_dish = await self.get_dish_by_id(dish_id)
        return updated_dish

    async def delete_dish_by_id(self, dish_id: str) -> bool:
        dish = await self.get_dish_by_id(dish_id)
        if dish:
            async with self.session as db_session:
                async with db_session.begin():
                    await self.session.delete(dish)
                    await self.session.commit()
            return True
        return False
