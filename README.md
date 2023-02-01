[![My Skills](https://skillicons.dev/icons?i=py,fastapi,postgres,redis,docker,github)](https://skillicons.dev)

# FastAPI_Menu

[![Maintainability](https://api.codeclimate.com/v1/badges/e9159925efd9c3308368/maintainability)](https://codeclimate.com/github/SadLaboka/FastAPI_Menu/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/e9159925efd9c3308368/test_coverage)](https://codeclimate.com/github/SadLaboka/FastAPI_Menu/test_coverage)
[![flake8](https://github.com/SadLaboka/FastAPI_Menu/actions/workflows/flake8.yml/badge.svg)](https://github.com/SadLaboka/FastAPI_Menu/actions/workflows/flake8.yml)

Simple FastAPI API for a restaurant menu.

# Usage:
* ### Create environment variables from file .env.example

* ### 1. With Make:
     ```
     make run
     ```
  ### 2. Without Make:
     ```
     docker-compose up --build
     ```
  ### 3. Without Docker:
     ```
     python -m uvicorn main:app --host 0.0.0.0 --port 8000
     python -m alembic upgrade head
     ```
## .env example:
```
PROJECT_NAME=Menu
DBHOST=127.0.0.1       # must be postgres_db for docker
DBPORT=5432
DBUSER=postgres
DBPASSWORD=postgres
DBNAME=postgres
REDIS_HOST=localhost       # must be redis_cache for docker
REDIS_PORT=6379
REDIS_DB=0
CACHE_EXPIRE_IN_SECONDS=600
```

# Running tests:
 ### 1. With Make:
   ```
     make test
   ```
 ### 2. With Docker:
   ```
     docker-compose -f docker-compose-test.yaml up --build
   ```

# REST API

## Docs:
1. OpenAPI:
```
/api/openapi
```
2. Redoc:
```
/api/redoc
```


## Requests:

| Description           | Method                                            | Request                                                                |
|-----------------------|---------------------------------------------------|------------------------------------------------------------------------|
| Get menu list         |![GET](https://img.shields.io/badge/-GET-blue)     | `/api/v1/menus/`                                                       |
| Create a menu         |![POST](https://img.shields.io/badge/-POST-success)| `/api/v1/menus/`                                                       |
| Get a specific menu   |![GET](https://img.shields.io/badge/-GET-blue)     | `/api/v1/menus/{menu_id}`                                              |
| Delete a menu         |![DELETE](https://img.shields.io/badge/-DELETE-red)| `/api/v1/menus/{menu_id}`                                              |
| Update a menu         |![PATCH](https://img.shields.io/badge/-PATCH-9cf)  | `/api/v1/menus/{menu_id}`                                              |
| Get submenu list      |![GET](https://img.shields.io/badge/-GET-blue)     | `/api/v1/menus/{menu_id}/submenus`                                     |
| Create a submenu      |![POST](https://img.shields.io/badge/-POST-success)| `/api/v1/menus/{menu_id}/submenus`                                     |
| Get a specific submenu|![GET](https://img.shields.io/badge/-GET-blue)     | `/api/v1/menus/{menu_id}/submenus/{submenu_id}`                        |
| Delete a submenu      |![DELETE](https://img.shields.io/badge/-DELETE-red)| `/api/v1/menus/{menu_id}/submenus/{submenu_id}`                        |
| Update a submenu      |![PATCH](https://img.shields.io/badge/-PATCH-9cf)  | `/api/v1/menus/{menu_id}/submenus/{submenu_id}`                        |
| Get dishes list       |![GET](https://img.shields.io/badge/-GET-blue)     | `/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes`                 |
| Create a dish         |![POST](https://img.shields.io/badge/-POST-success)| `/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes`                 |
| Get a specific dish   |![GET](https://img.shields.io/badge/-GET-blue)     | `/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}`       |
| Delete a dish         |![DELETE](https://img.shields.io/badge/-DELETE-red)| `/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}`       |
| Update a dish         |![PATCH](https://img.shields.io/badge/-PATCH-9cf)  | `/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}`       |
