from uuid import UUID

from pydantic import BaseModel

__all__ = (
    "MenuResponse",
    "MenuListResponse",
    "MenuCreate",
    "MenuUpdate"
)


class MenuBase(BaseModel):
    title: str
    description: str


class MenuResponse(MenuBase):
    id: UUID
    submenus_count: int
    dishes_count: int


class MenuCreate(MenuBase):
    ...


class MenuUpdate(MenuBase):
    ...


class MenuListResponse(BaseModel):
    menus: list[MenuResponse] = []
