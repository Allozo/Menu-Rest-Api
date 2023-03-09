# Menu-Rest-Api

## Жизнь без Docker

### Установка зависимостей

Для установки всех необходимых зависимостей (из файла `pyproject.toml`) воспользуйтесь командой:

```shell
poetry install
```

### Запуск приложения

Для запуска приложения воспользуйтесь командой:

```shell
poetry run uvicorn menu.main:app
```

По умолчанию БД будет `sqlite`.

После этого можно перейти по [ссылке](http://127.0.0.1:8000/docs), чтобы увидеть все доступные методы.

### Запуск тестов Postman

Для запуска тестов скачайте Postman, импортируйте туда два файла из папки `tests`, выберите окружение и запустите все тесты.

### Запуск тестов через pytest

На Linux:

```shell
SQLALCHEMY_SILENCE_UBER_WARNING=1 poetry run pytest tests/
```

На Windows:

```shell
set SQLALCHEMY_SILENCE_UBER_WARNING=1
poetry run pytest tests/
```

## Жизнь с Docker

### Запуск контейнера с приложением (БД sqlite)

По умолчанию БД будет `sqlite`.

Сборка образа:

```shell
docker build -t menu_app .
```

Запуск контейнера:

```shell
docker run --name flask_app_menu -p 8000:8000 -d menu_app
```

После этого можно перейти по [ссылке](http://127.0.0.1:8000/docs), чтобы увидеть все доступные методы.

### Запуск приложения через Docker-Compose

Используется `PostgreSQL`.

Создание и запуск всех контейнеров осуществляется командой:

```shell
docker-compose up --build -d
```

### Запуск тестов с помощью Docker-Compose

Создание и запуск контейнера, который запустит тесты осуществляется командой:

```shell
docker-compose -f docker-compose.test.yaml up --build
```

После этого можно перейти по [ссылке](http://127.0.0.1:8000/docs), чтобы увидеть все доступные методы.
