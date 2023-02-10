from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    description: str
    price: str


class Dish(DishBase):
    id: str
    menu_id: str
    submenu_id: str

    class Config:
        orm_mode = True


class SubmenuBase(BaseModel):
    title: str
    description: str


class Submenu(SubmenuBase):
    id: str
    menu_id: str
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
