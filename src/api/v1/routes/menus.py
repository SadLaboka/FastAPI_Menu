from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.schemas import MenuCreate, MenuResponse, MenuUpdate
from src.api.v1.schemas.menus import (SubMenuCreate, SubMenuResponse,
                                      SubMenuUpdate)
from src.services import MenuService, get_menu_service

router = APIRouter()


@router.get(
    path="/",
    summary="Get menu list",
    tags=["menus"],
)
async def menu_list(service: MenuService = Depends(get_menu_service)):
    menus: list = await service.get_menu_list()
    return menus


@router.get(
    path="/{menu_id}",
    response_model=MenuResponse,
    summary="Get a specific menu",
    tags=["menus"]
)
async def menu_detail(
        menu_id: str,
        service: MenuService = Depends(get_menu_service)
) -> MenuResponse:
    menu: Optional[dict] = await service.get_menu(menu_id)
    if not menu:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="menu not found")
    return MenuResponse(**menu)


@router.post(
    path="/",
    response_model=MenuResponse,
    status_code=HTTPStatus.CREATED,
    summary="Create a menu",
    tags=["menus"]
)
async def menu_create(
        menu: MenuCreate,
        service: MenuService = Depends(get_menu_service)
) -> MenuResponse:
    menu: dict = await service.create_menu(menu)
    return MenuResponse(**menu)


@router.patch(
    path="/{menu_id}",
    response_model=MenuResponse,
    summary="Update a menu",
    tags=["menus"]
)
async def menu_update(
        menu_id: str,
        new_data: MenuUpdate,
        service: MenuService = Depends(get_menu_service)
) -> MenuResponse:
    menu: Optional[dict] = await service.update_menu(menu_id, new_data)
    if not menu:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="menu not found")
    return MenuResponse(**menu)


@router.delete(
    path="/{menu_id}",
    summary="Delete a menu",
    tags=["menus"]
)
async def menu_delete(
        menu_id: str,
        service: MenuService = Depends(get_menu_service)
) -> dict:
    result: bool = await service.delete_menu(menu_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="menu not found")
    return {"status": True, "message": "The menu has been deleted"}


@router.get(
    path="/{menu_id}/submenus",
    summary="Get submenu list",
    tags=["menus"]
)
async def submenu_list(
        menu_id: str,
        service: MenuService = Depends(get_menu_service)
) -> list:
    submenus = await service.get_submenus(menu_id=menu_id)
    return submenus


@router.get(
    path="/{menu_id}/submenus/{submenu_id}",
    response_model=SubMenuResponse,
    summary="Get a specific submenu",
    tags=["menus"]
)
async def submenu_detail(
        submenu_id: str,
        service: MenuService = Depends(get_menu_service)
) -> SubMenuResponse:
    submenu: dict = await service.get_submenu(submenu_id=submenu_id)
    if not submenu:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="submenu not found")
    return SubMenuResponse(**submenu)


@router.post(
    path="/{menu_id}/submenus",
    response_model=SubMenuResponse,
    status_code=HTTPStatus.CREATED,
    summary="Create a submenu",
    tags=["menus"]
)
async def submenu_create(
        menu_id: str,
        submenu: SubMenuCreate,
        service: MenuService = Depends(get_menu_service)
) -> SubMenuResponse:
    submenu: dict = await service.create_submenu(menu_id=menu_id, submenu=submenu)
    if not submenu:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="menu not found")
    return SubMenuResponse(**submenu)


@router.patch(
    path="/{menu_id}/submenus/{submenu_id}",
    response_model=SubMenuResponse,
    summary="Update a submenu",
    tags=["menus"]
)
async def submenu_update(
        submenu_id: str,
        new_data: SubMenuUpdate,
        service: MenuService = Depends(get_menu_service)
) -> SubMenuResponse:
    submenu = await service.update_submenu(submenu_id=submenu_id, new_data=new_data)
    if not submenu:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="submenu not found")
    return SubMenuResponse(**submenu)


@router.delete(
    path="/{menu_id}/submenus/{submenu_id}",
    summary="Delete a submenu",
    tags=["menus"]
)
async def submenu_delete(
        submenu_id: str,
        service: MenuService = Depends(get_menu_service)
) -> dict:
    result: bool = await service.delete_submenu(submenu_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="submenu not found")
    return {"status": True, "message": "The submenu has been deleted"}
