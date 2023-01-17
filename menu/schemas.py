from pydantic import BaseModel


class Dish(BaseModel):
    id: str
    title: str
    description: str
    price: float

    class Config:
        orm_mode = True


class SubmenuBase(BaseModel):
    title: str
    description: str


class Submenu(SubmenuBase):
    id: str
    dishes_count: int

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
