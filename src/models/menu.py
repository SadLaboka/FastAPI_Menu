import uuid

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db import db_base


class MenuModel(db_base):
    __tablename__ = "menu"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(60), nullable=False, unique=False)
    description = Column(String(200), nullable=True, unique=False)
    menu_id = Column(
        UUID,
        ForeignKey("menu.id", ondelete="CASCADE"), nullable=False
    )
    menu = relationship("MenuModel", back_populates="submenus")
    dishes = relationship("DishModel", back_populates="submenu")


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
