from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi_versioning import VersionedFastAPI, version
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Any, Union
from . import models, schemas

from . import crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/menus", response_model=list[schemas.Menu])
@version(1)
def get_all_menu(db: Session = Depends(get_db)):
    return crud.get_all_menu(db)


@app.get(
    "/menus/{menu_id}",
    response_model=schemas.Menu,
)
@version(1)
def get_menu_by_id(menu_id: str, db: Session = Depends(get_db)):
    menu_db = crud.get_menu_by_id(menu_id, db)

    if menu_db is None:
        return JSONResponse(
            status_code=404, content={"detail": "menu not found"}
        )

    return menu_db


@app.post("/menus", response_model=schemas.Menu, status_code=201)
@version(1)
def create_menu(menu: schemas.MenuBase, db: Session = Depends(get_db)):
    return crud.create_menu(menu, db)


@app.delete("/menus/{menu_id}")
@version(1)
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    crud.delete_menu(menu_id, db)
    return JSONResponse(
        status_code=200,
        content={"status": True, "message": "The menu has been deleted"},
    )


@app.patch("/menus/{menu_id}", response_model=schemas.Menu)
@version(1)
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


@app.get("/menus/{menu_id}/submenus", response_model=list[schemas.Submenu])
@version(1)
def get_all_submenu_for_menu(menu_id: str, db: Session = Depends(get_db)):
    return crud.get_all_submenu(menu_id, db)


@app.get(
    "/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.Submenu
)
@version(1)
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
    "/menus/{menu_id}/submenus", response_model=schemas.Submenu, status_code=201
)
@version(1)
def create_submenu(
    menu_id: str, submenu: schemas.SubmenuBase, db: Session = Depends(get_db)
):
    submenu_db = crud.create_submenu(menu_id, submenu, db)
    return submenu_db


@app.patch(
    "/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.Submenu
)
@version(1)
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

    menu_db = crud.update_submenu(submenu_db, new_submenu, db)
    return menu_db


@app.delete("/menus/{menu_id}/submenus/{submenu_id}")
@version(1)
def delete_submenu(
    menu_id: str, submenu_id: str, db: Session = Depends(get_db)
):
    crud.delete_submenu(menu_id, submenu_id, db)
    return JSONResponse(
        status_code=200,
        content={"status": True, "message": "The submenu has been deleted"},
    )


app = VersionedFastAPI(
    app, version_format="{major}", prefix_format="/api/v{major}"
)
