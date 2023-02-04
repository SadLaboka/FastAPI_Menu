import json

import aiofiles  # type: ignore
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from celery import Celery
from celery.result import AsyncResult
from src.accessors import MenuAccessor, MenuCacheAccessor
from src.api.v1.schemas import (
    DishCreate,
    DishUpdate,
    MenuCreate,
    MenuUpdate,
    SubMenuCreate,
    SubMenuUpdate,
)
from src.core import config
from src.db import get_session
from src.db.cache import AbstractCache, get_cache
from src.models import Dish, Menu, SubMenu
from src.services.mixins import ServiceMixin

celery_app = Celery("tasks", broker=config.RABBITMQ_URL, backend="rpc://")


class MenuService(ServiceMixin):
    async def create_menu(self, menu: MenuCreate) -> dict | None:
        """Creates a new menu."""
        new_menu = await self.accessor.create_menu(
            title=menu.title, description=menu.description
        )
        if new_menu:
            answer = await self.make_menu_answer(new_menu)
            await self.cache_accessor.set_item(type_="menu", item=answer)
            await self.cache_accessor.delete_list("menus")
            return answer
        return None

    async def delete_menu(self, menu_id: str) -> bool:
        """Deletes menu by given id."""
        result = await self.accessor.delete_menu_by_id(id_=menu_id)
        await self.cache_accessor.delete(type_="menu", id_=menu_id)
        await self.cache_accessor.delete_list("menus")
        return result

    async def get_menu(self, menu_id: str) -> dict | None:
        """Gets a menu for a given id."""
        cached_menu = await self.cache_accessor.get_item(type_="menu", id_=menu_id)
        if cached_menu:
            return cached_menu
        menu = await self.accessor.get_menu_by_id(id_=menu_id)
        if menu:
            answer = await self.make_menu_answer(menu)
            await self.cache_accessor.set_item(type_="menu", item=answer)
            return answer
        return None

    async def get_menu_list(self) -> list[dict]:
        """Gets a menu list."""
        cached_menus = await self.cache_accessor.get_list("menus")
        if cached_menus:
            return cached_menus

        menus = await self.accessor.get_menus()
        menus_list = [await self.make_menu_answer(menu) for menu in menus]
        await self.cache_accessor.set_list("menus", menus_list)
        return menus_list

    async def update_menu(self, menu_id: str, new_data: MenuUpdate) -> dict | None:
        """Updates a menu for a given id."""
        menu = await self.accessor.update_menu(
            id_=menu_id,
            title=new_data.title,
            description=new_data.description,
        )
        if menu:
            answer = await self.make_menu_answer(menu)
            await self.cache_accessor.set_item(type_="menu", item=answer)
            await self.cache_accessor.delete_list("menus")
            return answer
        return None

    async def create_submenu(self, menu_id: str, submenu: SubMenuCreate) -> dict | None:
        """Creates a new submenu."""
        new_submenu = await self.accessor.create_submenu(
            menu_id=menu_id,
            title=submenu.title,
            description=submenu.description,
        )
        if new_submenu:
            answer = await self.make_submenu_answer(new_submenu)
            await self.cache_accessor.set_item(type_="submenu", item=answer)
            await self.cache_accessor.delete_list("submenus")
            await self.cache_accessor.delete_list("menus")
            await self.cache_accessor.delete(type_="menu", id_=menu_id)
            return answer
        return None

    async def delete_submenu(self, menu_id: str, submenu_id: str) -> bool:
        """Deletes submenu by given id."""
        result = await self.accessor.delete_submenu_by_id(id_=submenu_id)
        await self.cache_accessor.delete(type_="submenu", id_=submenu_id)
        await self.cache_accessor.delete_list("submenus")
        await self.cache_accessor.delete_list("menus")
        await self.cache_accessor.delete(type_="menu", id_=menu_id)

        return result

    async def get_submenu(self, submenu_id: str) -> dict | None:
        """Gets a submenu for a given id."""
        cached_submenu = await self.cache_accessor.get_item(
            type_="submenu", id_=submenu_id
        )
        if cached_submenu:
            return cached_submenu
        submenu = await self.accessor.get_submenu_by_id(id_=submenu_id)
        if submenu:
            answer = await self.make_submenu_answer(submenu)
            await self.cache_accessor.set_item(type_="submenu", item=answer)
            return answer
        return None

    async def get_submenus(self, menu_id: str) -> list[dict]:
        """Gets a submenu list."""
        cached_submenus = await self.cache_accessor.get_list("submenus")
        if cached_submenus:
            return cached_submenus
        submenus = await self.accessor.get_submenus(menu_id=menu_id)
        submenus_list = [
            await self.make_submenu_answer(submenu) for submenu in submenus
        ]
        await self.cache_accessor.set_list(key="submenus", items=submenus_list)
        return submenus_list

    async def update_submenu(
        self, submenu_id: str, new_data: SubMenuUpdate
    ) -> dict | None:
        """Updates a submenu for a given id."""
        submenu = await self.accessor.update_submenu(
            id_=submenu_id,
            title=new_data.title,
            description=new_data.description,
        )
        if submenu:
            answer = await self.make_submenu_answer(submenu)
            await self.cache_accessor.set_item(type_="submenu", item=answer)
            await self.cache_accessor.delete_list("submenus")
            return answer
        return None

    async def create_dish(
        self, menu_id: str, submenu_id: str, dish: DishCreate
    ) -> dict | None:
        """Creates a new dish."""
        new_dish = await self.accessor.create_dish(
            submenu_id=submenu_id,
            title=dish.title,
            description=dish.description,
            price=dish.price,
        )

        if new_dish:
            answer = await self.make_dish_answer(new_dish)
            await self.cache_accessor.set_item(type_="dish", item=answer)
            await self.cache_accessor.delete_list("submenus")
            await self.cache_accessor.delete_list("menus")
            await self.cache_accessor.delete_list("dishes")
            await self.cache_accessor.delete(type_="menu", id_=menu_id)
            await self.cache_accessor.delete(type_="submenu", id_=submenu_id)
            return answer
        return None

    async def delete_dish(self, menu_id: str, submenu_id: str, dish_id: str) -> bool:
        """Deletes dish by given id."""
        result = await self.accessor.delete_dish_by_id(dish_id=dish_id)
        await self.cache_accessor.delete_list("submenus")
        await self.cache_accessor.delete_list("menus")
        await self.cache_accessor.delete_list("dishes")
        await self.cache_accessor.delete(type_="menu", id_=menu_id)
        await self.cache_accessor.delete(type_="submenu", id_=submenu_id)
        await self.cache_accessor.delete(type_="dish", id_=dish_id)

        return result

    async def get_dish(self, dish_id: str) -> dict | None:
        """Gets a dish for a given id."""
        cached_dish = await self.cache_accessor.get_item(type_="dish", id_=dish_id)
        if cached_dish:
            return cached_dish
        dish = await self.accessor.get_dish_by_id(dish_id=dish_id)

        if dish:
            answer = await self.make_dish_answer(dish)
            await self.cache_accessor.set_item(type_="dish", item=answer)
            return answer
        return None

    async def get_dishes(self, submenu_id: str) -> list[dict]:
        """Gets a dish list"""
        cached_dishes = await self.cache_accessor.get_list("dishes")
        if cached_dishes:
            return cached_dishes
        dishes = await self.accessor.get_dishes(submenu_id=submenu_id)
        dishes_list = [await self.make_dish_answer(dish) for dish in dishes]
        await self.cache_accessor.set_list("dishes", dishes_list)
        return dishes_list

    async def update_dish(self, dish_id: str, new_data: DishUpdate) -> dict | None:
        """Updates a dish for a given id."""
        dish = await self.accessor.update_dish(
            dish_id=dish_id,
            title=new_data.title,
            description=new_data.description,
            price=new_data.price,
        )

        if dish:
            answer = await self.make_dish_answer(dish)
            await self.cache_accessor.set_item(type_="dish", item=answer)
            await self.cache_accessor.delete_list("dishes")
            return answer
        return None

    async def generate_menus(self) -> None:
        """Reads test menus from file and populates the database with them."""
        async with aiofiles.open("src/data/menu.json", mode="r") as f:
            content = await f.read()

        menus = json.loads(content)
        await self.accessor.menu_multiple_create(menus)

        submenus = [submenu for menu in menus for submenu in menu["submenus"]]
        await self.accessor.submenu_multiple_create(submenus)

        dishes = [dish for submenu in submenus for dish in submenu["dishes"]]
        await self.accessor.dish_multiple_create(dishes)

    async def make_xl_file(self) -> str:
        """Sets the task to create an Excel file"""
        menus = await self.accessor.get_menus()
        menus_data = json.dumps([menu.to_dict() for menu in menus])
        result = celery_app.send_task(
            "tasks.create_xlsx_file", kwargs={"data": menus_data}
        )
        return result.id

    @staticmethod
    async def get_xl_file_status(task_id: str) -> AsyncResult:
        """Gets status of task by id"""
        result = celery_app.AsyncResult(id=task_id, app=celery_app)
        return result

    @staticmethod
    async def make_dish_answer(dish: Dish) -> dict:
        """Converts an object to the desired format"""
        return {
            "id": dish.id,
            "title": dish.title,
            "description": dish.description,
            "price": str(dish.price),
        }

    @staticmethod
    async def make_menu_answer(menu: Menu) -> dict:
        """Converts an object to the desired format"""
        return {
            "id": menu.id,
            "title": menu.title,
            "description": menu.description,
            "submenus_count": len(menu.submenus),
            "dishes_count": sum([len(submenu.dishes) for submenu in menu.submenus])
            if menu.submenus
            else 0,
        }

    @staticmethod
    async def make_submenu_answer(submenu: SubMenu) -> dict:
        """Converts an object to the desired format"""
        return {
            "id": submenu.id,
            "title": submenu.title,
            "description": submenu.description,
            "dishes_count": len(submenu.dishes),
        }


async def get_menu_service(
    session: AsyncSession = Depends(get_session),
    cache: AbstractCache = Depends(get_cache),
) -> MenuService:
    """Gets the menu-service instance for dependency injection."""
    accessor = MenuAccessor(session)
    cache_accessor = MenuCacheAccessor(cache)
    return MenuService(accessor=accessor, cache_accessor=cache_accessor)
