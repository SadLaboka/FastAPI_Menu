from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.accessors import MenuAccessor
from src.api.v1.schemas import (DishCreate, DishUpdate, MenuCreate, MenuUpdate,
                                SubMenuCreate, SubMenuUpdate)
from src.db import get_session
from src.models import Dish, Menu, SubMenu
from src.services.mixins import ServiceMixin


class MenuService(ServiceMixin):
    async def create_menu(self, menu: MenuCreate) -> dict:
        """Creates a new menu."""
        menu_accessor = MenuAccessor(self.session)
        new_menu = await menu_accessor.create_menu(title=menu.title, description=menu.description)

        answer = await self.make_menu_answer(new_menu)
        return answer

    async def delete_menu(self, menu_id: str) -> bool:
        """Deletes menu by given id."""
        menu_accessor = MenuAccessor(self.session)
        result = await menu_accessor.delete_menu_by_id(id_=menu_id)

        return result

    async def get_menu(self, menu_id: str) -> dict | None:
        """Gets a menu for a given id."""
        menu_accessor = MenuAccessor(self.session)
        menu = await menu_accessor.get_menu_by_id(id_=menu_id)
        if menu:
            answer = await self.make_menu_answer(menu)
            return answer

    async def get_menu_list(self) -> list[dict]:
        """Gets a menu list."""
        menu_accessor = MenuAccessor(self.session)
        menus = await menu_accessor.get_menus()

        return [await self.make_menu_answer(menu) for menu in menus]

    async def update_menu(self, menu_id: str, new_data: MenuUpdate) -> dict | None:
        """Updates a menu for a given id."""
        menu_accessor = MenuAccessor(self.session)
        menu = await menu_accessor.update_menu(
            id_=menu_id, title=new_data.title, description=new_data.description,
        )
        if menu:
            answer = await self.make_menu_answer(menu)
            return answer

    async def create_submenu(self, menu_id: str, submenu: SubMenuCreate) -> dict | None:
        """Creates a new submenu."""
        menu_accessor = MenuAccessor(self.session)
        submenu = await menu_accessor.create_submenu(
            menu_id=menu_id, title=submenu.title, description=submenu.description,
        )
        if submenu:
            answer = await self.make_submenu_answer(submenu)
            return answer

    async def delete_submenu(self, submenu_id: str) -> bool:
        """Deletes submenu by given id."""
        menu_accessor = MenuAccessor(self.session)
        result = await menu_accessor.delete_submenu_by_id(id_=submenu_id)

        return result

    async def get_submenu(self, submenu_id: str) -> dict | None:
        """Gets a submenu for a given id."""
        menu_accessor = MenuAccessor(self.session)
        submenu = await menu_accessor.get_submenu_by_id(id_=submenu_id)
        if submenu:
            answer = await self.make_submenu_answer(submenu)
            return answer

    async def get_submenus(self, menu_id: str) -> list[dict]:
        """Gets a submenu list."""
        menu_accessor = MenuAccessor(self.session)
        submenus = await menu_accessor.get_submenus(menu_id=menu_id)

        return [await self.make_submenu_answer(submenu) for submenu in submenus]

    async def update_submenu(self, submenu_id: str, new_data: SubMenuUpdate) -> dict | None:
        """Updates a submenu for a given id."""
        menu_accessor = MenuAccessor(self.session)
        submenu = await menu_accessor.update_submenu(
            id_=submenu_id, title=new_data.title, description=new_data.description,
        )
        if submenu:
            answer = await self.make_submenu_answer(submenu)
            return answer

    async def create_dish(self, submenu_id: str, dish: DishCreate) -> dict | None:
        """Creates a new dish."""
        menu_accessor = MenuAccessor(self.session)
        dish = await menu_accessor.create_dish(
            submenu_id=submenu_id, title=dish.title, description=dish.description, price=dish.price,
        )

        if dish:
            answer = await self.make_dish_answer(dish)
            return answer

    async def delete_dish(self, dish_id: str) -> bool:
        """Deletes dish by given id."""
        menu_accessor = MenuAccessor(self.session)
        result = await menu_accessor.delete_dish_by_id(dish_id=dish_id)

        return result

    async def get_dish(self, dish_id: str) -> dict | None:
        """Gets a dish for a given id."""
        menu_accessor = MenuAccessor(self.session)
        dish = await menu_accessor.get_dish_by_id(dish_id=dish_id)

        if dish:
            answer = await self.make_dish_answer(dish)
            return answer

    async def get_dishes(self, submenu_id: str) -> list[dict]:
        """Gets a dish list"""
        menu_accessor = MenuAccessor(self.session)
        dishes = await menu_accessor.get_dishes(submenu_id=submenu_id)

        return [await self.make_dish_answer(dish) for dish in dishes]

    async def update_dish(self, dish_id: str, new_data: DishUpdate) -> dict | None:
        """Updates a dish for a given id."""
        menu_accessor = MenuAccessor(self.session)
        dish = await menu_accessor.update_dish(
            dish_id=dish_id, title=new_data.title,
            description=new_data.description, price=new_data.price,
        )

        if dish:
            answer = await self.make_dish_answer(dish)
            return answer

    @staticmethod
    async def make_dish_answer(dish: Dish) -> dict:
        """Converts an object to the desired format"""
        return {
            'id': dish.id,
            'title': dish.title,
            'description': dish.description,
            'price': str(dish.price),
        }

    @staticmethod
    async def make_menu_answer(menu: Menu) -> dict:
        """Converts an object to the desired format"""
        return {
            'id': menu.id,
            'title': menu.title,
            'description': menu.description,
            'submenus_count': len(menu.submenus),
            'dishes_count': sum([len(submenu.dishes) for submenu in menu.submenus]) if menu.submenus else 0,
        }

    @staticmethod
    async def make_submenu_answer(submenu: SubMenu) -> dict:
        """Converts an object to the desired format"""
        return {
            'id': submenu.id,
            'title': submenu.title,
            'description': submenu.description,
            'dishes_count': len(submenu.dishes),
        }


async def get_menu_service(
        session: AsyncSession = Depends(get_session),
) -> MenuService:
    return MenuService(session=session)
