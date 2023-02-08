import json

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.db.cache import AbstractCache
from src.models import Dish, DishModel, Menu, MenuModel, SubMenu, SubMenuModel


class MenuCacheAccessor:
    def __init__(self, cache: AbstractCache):
        self.cache = cache

    async def set_item(self, type_: str, item: dict) -> None:
        """Generates a key and sets the item in the cache."""
        item_id = item["id"]
        key = f"{type_}:{item_id}"
        await self.cache.set(key, json.dumps(item))

    async def get_item(self, type_: str, id_: str) -> dict | None:
        """Generates a key and gets an item from the cache."""
        key = f"{type_}:{id_}"
        item = await self.cache.get(key)
        return json.loads(item) if item else None

    async def set_list(self, key: str, items: list):
        """Sets items to the cache by the given key."""
        await self.cache.set(key, json.dumps(items))

    async def get_list(self, key: str) -> list | None:
        """Gets items from the cache by the given key."""
        items = await self.cache.get(key)
        return json.loads(items) if items else None

    async def delete(self, type_: str, id_: str) -> None:
        """Generates a key and deletes the item from the cache."""
        await self.cache.remove(f"{type_}:{id_}")

    async def delete_list(self, key: str) -> None:
        """Deletes items from the cache by the given key."""
        await self.cache.remove(key)


class MenuAccessor:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def menu_multiple_create(self, menus_list: list[dict]) -> None:
        """Creates all menus from list"""
        menus = [
            MenuModel(
                id=menu["id"], title=menu["title"], description=menu["description"]
            )
            for menu in menus_list
        ]
        async with self.session as db_session:
            async with db_session.begin():
                self.session.add_all(menus)

    async def submenu_multiple_create(self, submenus_list: list[dict]) -> None:
        """Creates all submenus from list"""
        submenus = [
            SubMenuModel(
                id=submenu["id"],
                title=submenu["title"],
                description=submenu["description"],
                menu_id=submenu["menu_id"],
            )
            for submenu in submenus_list
        ]
        async with self.session as db_session:
            async with db_session.begin():
                self.session.add_all(submenus)

    async def dish_multiple_create(self, dishes_list: list[dict]) -> None:
        """Creates all submenus from list"""
        dishes = [
            DishModel(
                title=dish["title"],
                description=dish["description"],
                price=float(dish["price"]),
                submenu_id=dish["submenu_id"],
            )
            for dish in dishes_list
        ]
        async with self.session as db_session:
            async with db_session.begin():
                self.session.add_all(dishes)

    async def create_menu(self, title: str, description: str) -> Menu | None:
        """Creates a menu entry in the database."""
        menu = MenuModel(title=title, description=description)
        try:
            async with self.session as db_session:
                async with db_session.begin():
                    self.session.add(menu)
                    await self.session.flush()
        finally:
            new_menu = await self.get_menu_by_id(menu.id)
            return new_menu

    async def delete_menu_by_id(self, id_: str) -> bool:
        """Deletes a menu entry from the database."""
        async with self.session as db_session:
            async with db_session.begin():
                menu = (
                    await self.session.scalars(
                        select(MenuModel).where(MenuModel.id == id_),
                    )
                ).first()
                if menu:
                    await self.session.delete(menu)
                    await self.session.commit()
                    return True
        return False

    async def get_menu_by_id(self, id_: str) -> Menu | None:
        """Gets a menu entry from the database if it exists."""
        async with self.session as db_session:
            async with db_session.begin():
                menu = (
                    await self.session.scalars(
                        select(MenuModel)
                        .where(MenuModel.id == id_)
                        .options(
                            joinedload(MenuModel.submenus).joinedload(
                                SubMenuModel.dishes
                            )
                        ),
                    )
                ).first()
        return menu.to_dataclass() if menu else None

    async def get_menus(self) -> list[Menu]:
        """Gets a list of menus from the database."""
        async with self.session as db_session:
            async with db_session.begin():
                menus = await self.session.scalars(
                    select(MenuModel).options(
                        joinedload(MenuModel.submenus).joinedload(SubMenuModel.dishes)
                    ),
                )

        return [menu.to_dataclass() for menu in menus.unique()]

    async def update_menu(self, id_: str, title: str, description: str) -> Menu | None:
        """Updates a menu entry in the database."""
        async with self.session as db_session:
            async with db_session.begin():
                await self.session.execute(
                    update(MenuModel)
                    .where(
                        MenuModel.id == id_,
                    )
                    .values(
                        title=title,
                        description=description,
                    ),
                )
        updated_menu = await self.get_menu_by_id(id_)
        return updated_menu

    async def create_submenu(
        self, menu_id: str, title: str, description: str
    ) -> SubMenu | None:
        """Creates a submenu entry in the database."""
        submenu = SubMenuModel(title=title, description=description, menu_id=menu_id)
        try:
            async with self.session as db_session:
                async with db_session.begin():
                    self.session.add(submenu)
                    await self.session.flush()
        finally:
            new_submenu = await self.get_submenu_by_id(submenu.id)
            return new_submenu

    async def get_submenu_by_id(self, id_: str) -> SubMenu | None:
        """Gets a submenu entry from the database if it exists."""
        async with self.session as db_session:
            async with db_session.begin():
                submenu = (
                    await self.session.scalars(
                        select(SubMenuModel)
                        .where(SubMenuModel.id == id_)
                        .options(joinedload(SubMenuModel.dishes)),
                    )
                ).first()
        return submenu.to_dataclass() if submenu else None

    async def get_submenus(self, menu_id: str) -> list[SubMenu]:
        """Gets a list of submenus from the database."""
        async with self.session as db_session:
            async with db_session.begin():
                submenus = await self.session.scalars(
                    select(SubMenuModel)
                    .where(SubMenuModel.menu_id == menu_id)
                    .options(joinedload(SubMenuModel.dishes)),
                )

        return [submenu.to_dataclass() for submenu in submenus.unique()]

    async def update_submenu(
        self, id_: str, title: str, description: str
    ) -> SubMenu | None:
        """Updates a submenu entry in the database."""
        async with self.session as db_session:
            async with db_session.begin():
                await self.session.execute(
                    update(SubMenuModel)
                    .where(
                        SubMenuModel.id == id_,
                    )
                    .values(
                        title=title,
                        description=description,
                    ),
                )
        updated_submenu = await self.get_submenu_by_id(id_)
        return updated_submenu

    async def delete_submenu_by_id(self, id_: str) -> bool:
        """Deletes a submenu entry from the database."""
        async with self.session as db_session:
            async with db_session.begin():
                submenu = (
                    await self.session.scalars(
                        select(SubMenuModel).where(SubMenuModel.id == id_),
                    )
                ).first()
                if submenu:
                    await self.session.delete(submenu)
                    await self.session.commit()
                    return True
        return False

    async def create_dish(
        self, submenu_id: str, title: str, description: str, price: str
    ) -> Dish | None:
        """Creates a dish entry in the database."""
        dish = DishModel(
            submenu_id=submenu_id,
            title=title,
            description=description,
            price=float(price),
        )
        try:
            async with self.session as db_session:
                async with db_session.begin():
                    self.session.add(dish)
                    await self.session.flush()
        finally:
            return dish.to_dataclass() if dish.id else None

    async def get_dish_by_id(self, dish_id: str) -> Dish | None:
        """Gets a dish entry from the database if it exists."""
        async with self.session as db_session:
            async with db_session.begin():
                dish = (
                    await self.session.scalars(
                        select(DishModel).where(DishModel.id == dish_id),
                    )
                ).first()
        return dish.to_dataclass() if dish else None

    async def get_dishes(self, submenu_id: str) -> list[Dish]:
        """Gets a list of dishes from the database."""
        async with self.session as db_session:
            async with db_session.begin():
                dishes = await self.session.scalars(
                    select(DishModel).where(DishModel.submenu_id == submenu_id),
                )
        return [dish.to_dataclass() for dish in dishes.unique()]

    async def update_dish(
        self, dish_id: str, title: str, description: str, price: str
    ) -> Dish | None:
        """Updates a dish entry in the database."""
        async with self.session as db_session:
            async with db_session.begin():
                await self.session.execute(
                    update(DishModel)
                    .where(
                        DishModel.id == dish_id,
                    )
                    .values(
                        title=title,
                        description=description,
                        price=float(price),
                    ),
                )
        updated_dish = await self.get_dish_by_id(dish_id)
        return updated_dish

    async def delete_dish_by_id(self, dish_id: str) -> bool:
        """Deletes a dish entry from the database."""
        async with self.session as db_session:
            async with db_session.begin():
                dish = (
                    await self.session.scalars(
                        select(DishModel).where(DishModel.id == dish_id),
                    )
                ).first()
                if dish:
                    await self.session.delete(dish)
                    await self.session.commit()
                    return True
        return False
