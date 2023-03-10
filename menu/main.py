from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Any

from menu import models, schemas, crud
from menu.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/v1/menus", response_model=list[schemas.Menu])
def get_all_menu(db: Session = Depends(get_db)):
    return crud.get_all_menu(db)


@app.get(
    "/api/v1/menus/{menu_id}",
    response_model=schemas.Menu,
)
def get_menu_by_id(menu_id: str, db: Session = Depends(get_db)):
    menu_db = crud.get_menu_by_id(menu_id, db)

    if menu_db is None:
        return JSONResponse(
            status_code=404, content={"detail": "menu not found"}
        )

    return menu_db


@app.post("/api/v1/menus", response_model=schemas.Menu, status_code=201)
def create_menu(menu: schemas.MenuBase, db: Session = Depends(get_db)):
    return crud.create_menu(menu, db)


@app.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    crud.delete_menu(menu_id, db)
    return JSONResponse(
        status_code=200,
        content={"status": True, "message": "The menu has been deleted"},
    )


@app.patch("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
def update_menu(
    menu_id: str, menu_new: schemas.MenuBase, db: Session = Depends(get_db)
) -> Any:
    menu_db = crud.get_menu_by_id(menu_id, db)

    if menu_db is None:
        return JSONResponse(
            status_code=404, content={"detail": "menu not found"}
        )

    menu_db = crud.update_menu(menu_db, menu_new, db)
    return menu_db


@app.get(
    "/api/v1/menus/{menu_id}/submenus", response_model=list[schemas.Submenu]
)
def get_all_submenu_for_menu(menu_id: str, db: Session = Depends(get_db)):
    return crud.get_all_submenu(menu_id, db)


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.Submenu,
)
def get_submenu_for_menu_by_id(
    menu_id: str, submenu_id: str, db: Session = Depends(get_db)
):
    submenu_db = crud.get_submenu_by_id(menu_id, submenu_id, db)

    if submenu_db is None:
        return JSONResponse(
            status_code=404, content={"detail": "submenu not found"}
        )

    return submenu_db


@app.post(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=schemas.Submenu,
    status_code=201,
)
def create_submenu(
    menu_id: str, submenu: schemas.SubmenuBase, db: Session = Depends(get_db)
):
    submenu_db = crud.create_submenu(menu_id, submenu, db)
    return submenu_db


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.Submenu,
)
def update_submenu(
    menu_id: str,
    submenu_id: str,
    new_submenu: schemas.SubmenuBase,
    db: Session = Depends(get_db),
):
    submenu_db = crud.get_submenu_by_id(menu_id, submenu_id, db)

    if submenu_db is None:
        return JSONResponse(
            status_code=404, content={"detail": "submenu not found"}
        )

    submenu_db = crud.update_submenu(submenu_db, new_submenu, db)
    return submenu_db


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(
    menu_id: str, submenu_id: str, db: Session = Depends(get_db)
):
    crud.delete_submenu(menu_id, submenu_id, db)
    return JSONResponse(
        status_code=200,
        content={"status": True, "message": "The submenu has been deleted"},
    )


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=list[schemas.Dish],
)
def get_all_dish_for_submenu(
    menu_id: str, submenu_id: str, db: Session = Depends(get_db)
):
    return crud.get_all_dishes(menu_id, submenu_id, db)


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.Dish,
)
def get_dish_for_menu_by_id(
    menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)
):
    dish_db = crud.get_dish_by_id(menu_id, submenu_id, dish_id, db)

    if dish_db is None:
        return JSONResponse(
            status_code=404, content={"detail": "dish not found"}
        )

    return dish_db


@app.post(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=schemas.Dish,
    status_code=201,
)
def create_dish(
    menu_id: str,
    submenu_id: str,
    dish: schemas.DishBase,
    db: Session = Depends(get_db),
):
    dish_db = crud.create_dish(menu_id, submenu_id, dish, db)
    return dish_db


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.Dish,
)
def update_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    new_dish: schemas.DishBase,
    db: Session = Depends(get_db),
):
    dish_db = crud.get_dish_by_id(menu_id, submenu_id, dish_id, db)

    if dish_db is None:
        return JSONResponse(
            status_code=404, content={"detail": "dish not found"}
        )

    dish_db = crud.update_dish(dish_db, new_dish, db)
    return dish_db


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(
    menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)
):
    crud.delete_dish(menu_id, submenu_id, dish_id, db)
    return JSONResponse(
        status_code=200,
        content={"status": True, "message": "The dish has been deleted"},
    )
