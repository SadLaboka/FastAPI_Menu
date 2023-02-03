import re
from uuid import UUID

from pydantic import BaseModel, Field, validator

__all__ = (
    "DishResponse",
    "DishCreate",
    "DishUpdate",
    "MenuResponse",
    "MenuCreate",
    "MenuUpdate",
    "SubMenuResponse",
    "SubMenuCreate",
    "SubMenuUpdate",
)


class DishBase(BaseModel):
    title: str = Field(max_length=60)
    description: str = Field(max_length=200)
    price: str

    @validator("price")
    def check_price(cls, v):
        pattern = r"[+-]?([0-9]*[.])?[0-9]+"

        if not re.match(pattern, v):
            raise ValueError("Uncorrect price")
        return v


class DishResponse(DishBase):
    id: UUID


class DishCreate(DishBase):
    ...


class DishUpdate(DishBase):
    ...


class MenuBase(BaseModel):
    title: str = Field(max_length=60)
    description: str = Field(max_length=200)


class MenuResponse(MenuBase):
    id: UUID
    submenus_count: int
    dishes_count: int


class MenuCreate(MenuBase):
    ...


class MenuUpdate(MenuBase):
    ...


class SubMenuBase(BaseModel):
    title: str = Field(max_length=60)
    description: str = Field(max_length=200)


class SubMenuResponse(SubMenuBase):
    id: UUID
    dishes_count: int


class SubMenuCreate(SubMenuBase):
    ...


class SubMenuUpdate(SubMenuBase):
    ...
