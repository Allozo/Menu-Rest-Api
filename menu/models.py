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

    submenu = relationship(
        "Submenu",
        back_populates="menu",
        cascade="all, delete",
    )


class SubMenu(Base):
    __tablename__ = "submenu"

    id = Column(Integer, primary_key=True)
    title = Column(String(40), nullable=False, unique=True)
    description = Column(String(120), nullable=False, unique=True)
    dishes_count = Column(Integer, nullable=False)

    menu_id = Column(ForeignKey("menu.id"))

    menu = relationship("Menu", back_populates="submenu")
    dishes = relationship(
        "Dish",
        back_populates="submenu",
        cascade="all, delete",
    )


class Dish(Base):
    __tablename__ = "dish"

    id = Column(Integer, primary_key=True)
    title = Column(String(40), nullable=False, unique=True)
    description = Column(String(120), nullable=False, unique=True)
    price = Column(String(10), nullable=False)

    submenu_id = Column(ForeignKey("submenu.id"), nullable=False)

    submenu = relationship("SubMenu", back_populates="dishes")
