from uuid import UUID

from pydantic import BaseModel

__all__ = (
    "MenuResponse",
    "MenuCreate",
    "MenuUpdate",
    "SubMenuResponse",
    "SubMenuCreate",
    "SubMenuUpdate"
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


class SubMenuBase(BaseModel):
    title: str
    description: str


class SubMenuResponse(SubMenuBase):
    id: UUID
    dishes_count: int


class SubMenuCreate(SubMenuBase):
    ...


class SubMenuUpdate(SubMenuBase):
    ...
