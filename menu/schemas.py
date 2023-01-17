from pydantic import BaseModel


class Dish(BaseModel):
    id: int
    title: str
    description: str
    price: float

    class Config:
        orm_mode = True


class SubMenu(BaseModel):
    id: int
    title: str
    description: str
    dishes_count: int

    dishes: list[Dish]

    class Config:
        orm_mode = True


class Menu(BaseModel):
    id: int
    title: str
    description: str
    submenus_count: int
    dishes_count: int

    submenus: list[SubMenu]

    class Config:
        orm_mode = True