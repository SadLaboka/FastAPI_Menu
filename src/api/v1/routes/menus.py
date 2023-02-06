import os
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.exc import IntegrityError

from celery.result import AsyncResult
from src.api.v1.schemas import MenuCreate, MenuResponse, MenuUpdate
from src.api.v1.schemas.menus import (
    DishCreate,
    DishResponse,
    DishUpdate,
    SubMenuCreate,
    SubMenuResponse,
    SubMenuUpdate,
)
from src.core.config import BASE_DIR, BASE_URL
from src.services import MenuService, get_menu_service

router = APIRouter()


@router.get(
    path="/",
    summary="Get menu list",
    status_code=HTTPStatus.OK,
    tags=["menus"],
)
async def menu_list(service: MenuService = Depends(get_menu_service)):
    menus: list = await service.get_menu_list()
    return menus


@router.post(
    path="/make-xl-file",
    status_code=HTTPStatus.ACCEPTED,
    summary="Download menu to excel spreadsheet",
    tags=["Excel"],
)
async def make_xl(service: MenuService = Depends(get_menu_service)):
    task_id: str = await service.make_xl_file()
    return {"status": True, "message": f"Task added. Task_id = {task_id}"}


@router.get(
    path="/get-xl-file/{task_id}",
    status_code=HTTPStatus.OK,
    summary="Show status of file preparation and link to download",
    tags=["Excel"],
)
async def get_xl_status(task_id: str, service: MenuService = Depends(get_menu_service)):
    result: AsyncResult = await service.get_xl_file_status(task_id)
    if result.ready():
        return {
            "status": True,
            "message": f"Link to download file: {BASE_URL}/api/v1/menus/download/{task_id}",
        }
    return {
        "status": True,
        "message": f"File not ready yet. Task state is {result.state}",
    }


@router.get(
    path="/download/{filename}",
    status_code=HTTPStatus.OK,
    summary="Download file by filename",
    response_class=FileResponse,
    tags=["Excel"],
)
async def download_file(filename: str):
    headers = {"Content-Disposition": "attachment; filename=menu.xlsx"}
    return FileResponse(
        path=os.path.join(BASE_DIR.parent, "data", f"{filename}.xlsx"),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )


@router.post(
    path="/generate",
    status_code=HTTPStatus.OK,
    summary="Generate test menus and populate the database with them",
    tags=["generate"],
)
async def generate_menu(service: MenuService = Depends(get_menu_service)):
    try:
        await service.generate_menus()
    except IntegrityError as e:
        if e.orig.pgcode == "23505":
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Generated menus already exist"
            )
    return {"status": True, "message": "The database has been filled"}


@router.get(
    path="/{menu_id}",
    response_model=MenuResponse,
    summary="Get a specific menu",
    status_code=HTTPStatus.OK,
    tags=["menus"],
)
async def menu_detail(
    menu_id: str,
    service: MenuService = Depends(get_menu_service),
) -> MenuResponse:
    menu: dict | None = await service.get_menu(menu_id)
    if not menu:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="menu not found")
    return MenuResponse(**menu)


@router.post(
    path="/",
    response_model=MenuResponse,
    status_code=HTTPStatus.CREATED,
    summary="Create a menu",
    tags=["menus"],
)
async def menu_create(
    menu: MenuCreate,
    service: MenuService = Depends(get_menu_service),
) -> MenuResponse:
    menu_response: dict = await service.create_menu(menu)  # type: ignore
    return MenuResponse(**menu_response)


@router.patch(
    path="/{menu_id}",
    response_model=MenuResponse,
    summary="Update a menu",
    tags=["menus"],
)
async def menu_update(
    menu_id: str,
    new_data: MenuUpdate,
    service: MenuService = Depends(get_menu_service),
) -> MenuResponse:
    menu: dict | None = await service.update_menu(menu_id, new_data)
    if not menu:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="menu not found")
    return MenuResponse(**menu)


@router.delete(
    path="/{menu_id}",
    summary="Delete a menu",
    status_code=HTTPStatus.OK,
    tags=["menus"],
)
async def menu_delete(
    menu_id: str,
    service: MenuService = Depends(get_menu_service),
) -> dict:
    result: bool = await service.delete_menu(menu_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="menu not found")
    return {"status": True, "message": "The menu has been deleted"}


@router.get(
    path="/{menu_id}/submenus",
    summary="Get submenu list",
    status_code=HTTPStatus.OK,
    tags=["submenus"],
)
async def submenu_list(
    menu_id: str,
    service: MenuService = Depends(get_menu_service),
) -> list:
    submenus: list = await service.get_submenus(menu_id=menu_id)
    return submenus


@router.get(
    path="/{menu_id}/submenus/{submenu_id}",
    response_model=SubMenuResponse,
    summary="Get a specific submenu",
    status_code=HTTPStatus.OK,
    tags=["submenus"],
)
async def submenu_detail(
    submenu_id: str,
    service: MenuService = Depends(get_menu_service),
) -> SubMenuResponse:
    submenu: dict | None = await service.get_submenu(submenu_id=submenu_id)
    if not submenu:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="submenu not found"
        )
    return SubMenuResponse(**submenu)


@router.post(
    path="/{menu_id}/submenus",
    response_model=SubMenuResponse,
    status_code=HTTPStatus.CREATED,
    summary="Create a submenu",
    tags=["submenus"],
)
async def submenu_create(
    menu_id: str,
    submenu: SubMenuCreate,
    service: MenuService = Depends(get_menu_service),
) -> SubMenuResponse:
    submenu_response: dict | None = await service.create_submenu(
        menu_id=menu_id, submenu=submenu
    )
    if not submenu_response:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="menu not found")
    return SubMenuResponse(**submenu_response)


@router.patch(
    path="/{menu_id}/submenus/{submenu_id}",
    response_model=SubMenuResponse,
    summary="Update a submenu",
    status_code=HTTPStatus.OK,
    tags=["submenus"],
)
async def submenu_update(
    submenu_id: str,
    new_data: SubMenuUpdate,
    service: MenuService = Depends(get_menu_service),
) -> SubMenuResponse:
    submenu: dict | None = await service.update_submenu(
        submenu_id=submenu_id, new_data=new_data
    )
    if not submenu:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="submenu not found"
        )
    return SubMenuResponse(**submenu)


@router.delete(
    path="/{menu_id}/submenus/{submenu_id}",
    summary="Delete a submenu",
    status_code=HTTPStatus.OK,
    tags=["submenus"],
)
async def submenu_delete(
    menu_id: str,
    submenu_id: str,
    service: MenuService = Depends(get_menu_service),
) -> dict:
    result: bool = await service.delete_submenu(menu_id=menu_id, submenu_id=submenu_id)
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="submenu not found"
        )
    return {"status": True, "message": "The submenu has been deleted"}


@router.get(
    path="/{menu_id}/submenus/{submenu_id}/dishes",
    summary="Get dishes list",
    status_code=HTTPStatus.OK,
    tags=["dishes"],
)
async def dish_list(
    submenu_id: str,
    service: MenuService = Depends(get_menu_service),
) -> list:
    dishes: list = await service.get_dishes(submenu_id)
    return dishes


@router.get(
    path="/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=DishResponse,
    summary="Get a specific dish",
    status_code=HTTPStatus.OK,
    tags=["dishes"],
)
async def dish_detail(
    dish_id: str,
    service: MenuService = Depends(get_menu_service),
) -> DishResponse:
    dish: dict | None = await service.get_dish(dish_id)
    if not dish:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="dish not found")
    return DishResponse(**dish)


@router.patch(
    path="/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=DishResponse,
    summary="Update a dish",
    status_code=HTTPStatus.OK,
    tags=["dishes"],
)
async def dish_update(
    dish_id: str,
    new_data: DishUpdate,
    service: MenuService = Depends(get_menu_service),
) -> DishResponse:
    dish: dict | None = await service.update_dish(dish_id, new_data)
    if not dish:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="dish not found")
    return DishResponse(**dish)


@router.post(
    path="/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=DishResponse,
    status_code=HTTPStatus.CREATED,
    summary="Create a dish",
    tags=["dishes"],
)
async def dish_create(
    menu_id: str,
    submenu_id: str,
    dish: DishCreate,
    service: MenuService = Depends(get_menu_service),
) -> DishResponse:
    dish_response: dict | None = await service.create_dish(
        menu_id=menu_id, submenu_id=submenu_id, dish=dish
    )
    if not dish_response:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="dish not found")
    return DishResponse(**dish_response)


@router.delete(
    path="/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    summary="Delete a dish",
    status_code=HTTPStatus.OK,
    tags=["dishes"],
)
async def dish_delete(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    service: MenuService = Depends(get_menu_service),
) -> dict:
    result: bool = await service.delete_dish(
        menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
    )
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="dish not found")
    return {"status": True, "message": "The dish has been deleted"}
