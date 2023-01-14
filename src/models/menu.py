from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.db import db_base


class MenuModel(db_base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(60), nullable=False, unique=True)
    description = Column(String(200), nullable=True, unique=True)
    submenus = relationship(
        "SubMenuModel",
        back_populates="menu",
        cascade="all, delete",
        passive_deletes=True
    )


class SubMenuModel(db_base):
    __tablename__ = "submenu"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(60), nullable=False, unique=False)
    description = Column(String(200), nullable=True, unique=False)
    menu_id = Column(
        Integer,
        ForeignKey("menu.id", ondelete="CASCADE"), nullable=False
    )
    menu = relationship("MenuModel", back_populates="submenus")
    dishes = relationship("DishModel", back_populates="submenu")


class DishModel(db_base):
    __tablename__ = "dish"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(60), nullable=False, unique=False)
    description = Column(String(200), nullable=True, unique=False)
    price = Column(Float(2), nullable=False)
    submenu_id = Column(
        ForeignKey("submenu.id", ondelete="CASCADE"), nullable=False
    )
    submenu = relationship("SubMenuModel", back_populates="dishes")
