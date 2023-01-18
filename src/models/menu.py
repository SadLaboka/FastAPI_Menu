import uuid
from dataclasses import dataclass
from typing import List

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db import db_base


@dataclass
class Dish:
    id: uuid.UUID
    title: str
    description: str
    price: float


@dataclass
class SubMenu:
    id: uuid.UUID
    title: str
    description: str
    dishes: List[Dish]


@dataclass
class Menu:
    id: uuid.UUID
    title: str
    description: str
    submenus: List[SubMenu]


class MenuModel(db_base):
    __tablename__ = "menu"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(60), nullable=False, unique=True)
    description = Column(String(200), nullable=True, unique=False)
    submenus = relationship(
        "SubMenuModel",
        back_populates="menu",
        cascade="all, delete",
        passive_deletes=True
    )

    def to_dc(self) -> Menu:
        return Menu(
            id=self.id,
            title=self.title,
            description=self.description,
            submenus=[s.to_dc() for s in self.submenus]
        )


class SubMenuModel(db_base):
    __tablename__ = "submenu"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(60), nullable=False, unique=False)
    description = Column(String(200), nullable=True, unique=False)
    menu_id = Column(
        UUID,
        ForeignKey("menu.id", ondelete="CASCADE"), nullable=False
    )
    menu = relationship("MenuModel", back_populates="submenus")
    dishes = relationship(
        "DishModel",
        back_populates="submenu",
        cascade="all, delete",
        passive_deletes=True
    )

    def to_dc(self) -> SubMenu:
        return SubMenu(
            id=self.id,
            title=self.title,
            description=self.description,
            dishes=[d.to_dc() for d in self.dishes],
        )


class DishModel(db_base):
    __tablename__ = "dish"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(60), nullable=False, unique=False)
    description = Column(String(200), nullable=True, unique=False)
    price = Column(Float(2), nullable=False)
    submenu_id = Column(
        UUID,
        ForeignKey("submenu.id", ondelete="CASCADE"), nullable=False
    )
    submenu = relationship("SubMenuModel", back_populates="dishes")

    def to_dc(self) -> Dish:
        return Dish(
            id=self.id,
            title=self.title,
            description=self.description,
            price=self.price
        )
