from pydantic import BaseModel


class Dish(BaseModel):
    id: str
    title: str
    description: str
    price: float

    class Config:
        orm_mode = True


class SubMenu(BaseModel):
    id: str
    title: str
    description: str
    dishes_count: int

    dishes: list[Dish]

    class Config:
        orm_mode = True


class MenuBase(BaseModel):
    title: str
    description: str


class Menu(MenuBase):
    id: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True


class MenuNotFound(BaseModel):
    detail: str = "menu not found"
