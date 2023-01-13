from sqlalchemy import Column, Integer, String

from src.db import db_base


class MenuModel(db_base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(60), nullable=False, unique=True)
