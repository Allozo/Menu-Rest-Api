from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from menu.database import Base


class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True)
    title = Column(String(40), nullable=False, unique=True)
    description = Column(String(120), nullable=False, unique=True)
    submenus_count = Column(Integer, nullable=False)
    dishes_count = Column(Integer, nullable=False)

    submenus = relationship("SubMenu", back_populates="menu")


class SubMenu(Base):
    __tablename__ = "submenu"

    id = Column(Integer, primary_key=True)
    title = Column(String(40), nullable=False, unique=True)
    description = Column(String(120), nullable=False, unique=True)
    dishes_count = Column(Integer, nullable=False)

    menus = relationship("Menu", back_populates="submenu")
    dishes = relationship("Dish", back_populates="submenus")


class Dish(Base):
    __tablename__ = "dish"

    id = Column(Integer, primary_key=True)
    title = Column(String(40), nullable=False, unique=True)
    description = Column(String(120), nullable=False, unique=True)
    price = Column(Numeric(10, 2), nullable=False)

    submenu_id = Column(ForeignKey("submenu.id"), nullable=False)
