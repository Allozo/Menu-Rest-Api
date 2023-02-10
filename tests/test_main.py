from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from menu.main import app, get_db
from menu import models


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def test_db():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)


def test_get_menus():
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []


def test_post_menus():
    response1 = client.post(
        "/api/v1/menus",
        json={"title": "menu1", "description": "menu1_description"},
    )
    assert response1.status_code == 201
    assert response1.json() == {
        "title": "menu1",
        "description": "menu1_description",
        "id": "1",
        "submenus_count": 0,
        "dishes_count": 0,
    }

    client.post(
        "/api/v1/menus",
        json={"title": "menu2", "description": "menu2_description"},
    )

    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == [
        {
            "title": "menu1",
            "description": "menu1_description",
            "id": "1",
            "submenus_count": 0,
            "dishes_count": 0,
        },
        {
            "title": "menu2",
            "description": "menu2_description",
            "id": "2",
            "submenus_count": 0,
            "dishes_count": 0,
        },
    ]


def test_get_menu_error():
    response = client.get("/api/v1/menus/10")
    assert response.json() == {"detail": "menu not found"}
    assert response.status_code == 404


def test_get_menu_ok():
    client.post(
        "/api/v1/menus",
        json={"title": "menu1", "description": "menu1_description"},
    )
    response = client.get("/api/v1/menus/1")
    assert response.json() == {
        "title": "menu1",
        "description": "menu1_description",
        "id": "1",
        "submenus_count": 0,
        "dishes_count": 0,
    }
    assert response.status_code == 200


def test_update_menu():
    client.post(
        "/api/v1/menus",
        json={"title": "menu1", "description": "menu1_description"},
    )
    response = client.patch(
        "/api/v1/menus/1",
        json={
            "title": "menu2",
            "description": "menu2_description",
        },
    )
    assert response.json() == {
        "id": "1",
        "title": "menu2",
        "description": "menu2_description",
        "submenus_count": 0,
        "dishes_count": 0,
    }
    assert response.status_code == 200


def test_delete_menu():
    client.post(
        "/api/v1/menus",
        json={"title": "menu1", "description": "menu1_description"},
    )
    response = client.delete("/api/v1/menus/1")
    assert response.json() == {
        "status": True,
        "message": "The menu has been deleted",
    }
    assert response.status_code == 200


def test_get_submenu_empty():
    client.post(
        "/api/v1/menus",
        json={"title": "menu1", "description": "menu1_description"},
    )
    response = client.get("/api/v1/menus/1/submenus")
    assert response.json() == []


def test_create_submenu():
    client.post(
        "/api/v1/menus",
        json={"title": "menu1", "description": "menu1_description"},
    )
    response = client.post(
        "/api/v1/menus/1/submenus",
        json={"title": "submenu1", "description": "submenu1_description"},
    )
    assert response.json() == {
        "id": "1",
        "title": "submenu1",
        "description": "submenu1_description",
        "dishes_count": 0,
        "menu_id": "1",
    }
    assert response.status_code == 201


def test_get_submenu_ok():
    client.post(
        "/api/v1/menus",
        json={"title": "menu1", "description": "menu1_description"},
    )
    client.post(
        "/api/v1/menus/1/submenus",
        json={"title": "submenu1", "description": "submenu1_description"},
    )
    response = client.get("/api/v1/menus/1/submenus/1")
    assert response.json() == {
        "id": "1",
        "title": "submenu1",
        "description": "submenu1_description",
        "menu_id": "1",
        "dishes_count": 0,
    }
    assert response.status_code == 200


def test_get_submenu_error():
    client.post(
        "/api/v1/menus",
        json={"title": "menu1", "description": "menu1_description"},
    )
    response = client.get("/api/v1/menus/1/submenus/15")
    assert response.json() == {"detail": "submenu not found"}
    assert response.status_code == 404


def test_update_submenu():
    client.post(
        "/api/v1/menus",
        json={"title": "menu1", "description": "menu1_description"},
    )
    client.post(
        "/api/v1/menus/1/submenus",
        json={"title": "submenu1", "description": "submenu1_description"},
    )
    response = client.patch(
        "/api/v1/menus/1/submenus/1",
        json={"title": "submenu2", "description": "submenu2_description"},
    )

    assert response.json() == {
        "id": "1",
        "title": "submenu2",
        "description": "submenu2_description",
        "menu_id": "1",
        "dishes_count": 0,
    }
    assert response.status_code == 200


def test_delete_submenu():
    client.post(
        "/api/v1/menus",
        json={"title": "menu1", "description": "menu1_description"},
    )
    client.post(
        "/api/v1/menus/1/submenus",
        json={"title": "submenu1", "description": "submenu1_description"},
    )
    response = client.delete(
        "/api/v1/menus/1/submenus/1",
    )
    assert response.json() == {
        "status": True,
        "message": "The submenu has been deleted",
    }
    assert response.status_code == 200


def test_get_dishes():
    client.post(
        "/api/v1/menus",
        json={"title": "menu1", "description": "menu1_description"},
    )
    client.post(
        "/api/v1/menus/1/submenus",
        json={"title": "submenu1", "description": "submenu1_description"},
    )
    response = client.get("/api/v1/menus/1/submenus/1/dishes")
    assert response.json() == []


def test_create_dishes():
    client.post(
        "/api/v1/menus",
        json={"title": "menu1", "description": "menu1_description"},
    )
    client.post(
        "/api/v1/menus/1/submenus",
        json={"title": "submenu1", "description": "submenu1_description"},
    )
    response = client.post(
        "/api/v1/menus/1/submenus/1/dishes",
        json={
            "title": "dish1",
            "description": "dish1_description",
            "price": "100",
        },
    )
    assert response.json() == {
        "id": "1",
        "menu_id": "1",
        "submenu_id": "1",
        "price": "100",
        "title": "dish1",
        "description": "dish1_description",
    }
    assert response.status_code == 201


def test_get_dishes_error():
    client.post(
        "/api/v1/menus",
        json={"title": "menu1", "description": "menu1_description"},
    )
    client.post(
        "/api/v1/menus/1/submenus",
        json={"title": "submenu1", "description": "submenu1_description"},
    )
    client.get("/api/v1/menus/1/submenus/1/dishes/20")
    response = client.get("/menus/1/submenus/1/dishes/20")
    assert response.status_code == 404


def test_get_dishes_ok():
    id_menu = client.post(
        "/api/v1/menus",
        json={"title": "menu1", "description": "menu1_description"},
    ).json()["id"]
    client.post(
        "/api/v1/menus/1/submenus",
        json={"title": "submenu1", "description": "submenu1_description"},
    )
    client.post(
        "/api/v1/menus/1/submenus/1/dishes",
        json={
            "title": "dish1",
            "description": "dish1_description",
            "price": "100",
        },
    )
    response = client.get("api/v1/menus/1/submenus/1/dishes/1")
    assert response.json() == {
        "id": "1",
        "title": "dish1",
        "description": "dish1_description",
        "menu_id": "1",
        "submenu_id": "1",
        "price": "100",
    }
    assert response.status_code == 200


def test_update_dishes_ok():
    client.post(
        "/api/v1/menus",
        json={"title": "menu1", "description": "menu1_description"},
    )
    client.post(
        "/api/v1/menus/1/submenus",
        json={"title": "submenu1", "description": "submenu1_description"},
    )
    client.post(
        "/api/v1/menus/1/submenus/1/dishes",
        json={
            "title": "dish1",
            "description": "dish1_description",
            "price": "100",
        },
    )
    response = client.patch(
        "/api/v1/menus/1/submenus/1/dishes/1",
        json={
            "title": "dish2",
            "description": "dish2_description",
            "price": "200",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "title": "dish2",
        "description": "dish2_description",
        "menu_id": "1",
        "submenu_id": "1",
        "price": "200",
    }


def test_delete_dishes():
    client.post(
        "/api/v1/menus",
        json={"title": "menu1", "description": "menu1_description"},
    )
    client.post(
        "/api/v1/menus/1/submenus",
        json={"title": "submenu1", "description": "submenu1_description"},
    )
    client.post(
        "/api/v1/menus/1/submenus/1/dishes",
        json={
            "title": "dish1",
            "description": "dish1_description",
            "price": "100",
        },
    )
    response = client.delete(
        "/api/v1/menus/1/submenus/1/dishes/1",
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": True,
        "message": "The dish has been deleted",
    }
