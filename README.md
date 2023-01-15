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
     docker-compose exec api python -m alembic upgrade head
     ```
  ### 3. Without Docker:
     ```
     python -m uvicorn main:app --host 0.0.0.0 --port 8000
     python -m alembic upgrade head
     ```


# REST API

## Requests:

| Description                                                            | Request                                                                |
|------------------------------------------------------------------------|------------------------------------------------------------------------|
| Get menu list                                                          | `GET /api/v1/menus/`                                                   |
| Create a menu                                                          | `POST /api/v1/menus/`                                                  |
| Get a specific menu                                                    | `GET /api/v1/menus/{menu_id}`                                          |
| Delete a menu                                                          | `DELETE /api/v1/menus/{menu_id}`                                       |
| Update a menu                                                          | `PATCH /api/v1/menus/{menu_id}`                                        |
| Get submenu list                                                       | `GET /api/v1/menus/{menu_id}/submenus`                                 |
| Create a submenu                                                       | `POST /api/v1/menus/{menu_id}/submenus`                                |
| Get a specific submenu                                                 | `GET /api/v1/menus/{menu_id}/submenus/{submenu_id}`                    |
| Delete a submenu                                                       | `DELETE /api/v1/menus/{menu_id}/submenus/{submenu_id}`                 |
| Update a submenu                                                       | `PATCH /api/v1/menus/{menu_id}/submenus/{submenu_id}`                  |
| Get dishes list                                                        | `GET /api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes`             |
| Create a dish                                                          | `POST /api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes`            |
| Get a specific dish                                                    | `GET /api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}`   |
| Delete a dish                                                          | `DELETE /api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}`|
| Update a dish                                                          | `PATCH /api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}` |
