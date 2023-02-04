import uuid
from dataclasses import dataclass

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db import db_base


@dataclass
class Dish:
    id: str
    title: str
    description: str
    price: float

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
        }


@dataclass
class SubMenu:
    id: str
    title: str
    description: str
    dishes: list[Dish]

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "dishes": [dish.to_dict() for dish in self.dishes],
        }


@dataclass
class Menu:
    id: str
    title: str
    description: str
    submenus: list[SubMenu]

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "submenus": [submenu.to_dict() for submenu in self.submenus],
        }


class MenuModel(db_base):
    __tablename__ = "menu"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(60), nullable=False, unique=True)
    description = Column(String(200), nullable=True, unique=False)
    submenus = relationship(
        "SubMenuModel",
        back_populates="menu",
        cascade="all, delete",
        passive_deletes=True,
    )

    def to_dc(self) -> Menu:
        return Menu(
            id=str(self.id),
            title=self.title,
            description=self.description,
            submenus=[s.to_dc() for s in self.submenus],
        )


class SubMenuModel(db_base):
    __tablename__ = "submenu"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(60), nullable=False, unique=False)
    description = Column(String(200), nullable=True, unique=False)
    menu_id = Column(
        UUID,
        ForeignKey("menu.id", ondelete="CASCADE"),
        nullable=False,
    )
    menu = relationship("MenuModel", back_populates="submenus")
    dishes = relationship(
        "DishModel",
        back_populates="submenu",
        cascade="all, delete",
        passive_deletes=True,
    )

    def to_dc(self) -> SubMenu:
        return SubMenu(
            id=str(self.id),
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
        ForeignKey("submenu.id", ondelete="CASCADE"),
        nullable=False,
    )
    submenu = relationship("SubMenuModel", back_populates="dishes")

    def to_dc(self) -> Dish:
        return Dish(
            id=str(self.id),
            title=self.title,
            description=self.description,
            price=self.price,
        )
