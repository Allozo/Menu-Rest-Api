from sqlalchemy.orm import Session

from menu import models, schemas


def get_all_menu(db: Session) -> list[schemas.MenuBase]:
    res = db.query(models.Menu).all()
    return res


def get_menu_by_id(menu_id: str, db: Session) -> schemas.Menu:
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()


def create_menu(menu: schemas.MenuBase, db: Session) -> schemas.Menu:
    menu_db = models.Menu(
        title=menu.title,
        description=menu.description,
        submenus_count=0,
        dishes_count=0,
    )
    db.add(menu_db)
    db.commit()
    db.refresh(menu_db)
    return menu_db


def delete_menu(menu_id: str, db: Session) -> None:
    menu_db = get_menu_by_id(menu_id, db)
    db.delete(menu_db)
    db.commit()


def update_menu(
    old_menu, new_menu: schemas.MenuBase, db: Session
) -> schemas.MenuBase:
    old_menu.title, old_menu.description = new_menu.title, new_menu.description
    db.add(old_menu)
    db.commit()
    db.refresh(old_menu)
    return old_menu
