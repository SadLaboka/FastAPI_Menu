from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, HTTPException

from src.api.v1.schemas import (MenuCreate, MenuListResponse, MenuResponse,
                                MenuUpdate)

router = APIRouter()


@router.get(
    path="/",
    response_model=MenuListResponse,
    summary="Get menu list",
    tags=["menus"],
)
async def menu_list() -> MenuListResponse:
    menus: dict = dict()
    return MenuListResponse(**menus)


@router.get(
    path="/{menu_id}",
    response_model=MenuResponse,
    summary="Get a specific menu",
    tags=["menus"]
)
async def menu_detail(
        menu_id: int
) -> MenuResponse:
    menu: Optional[dict] = dict()
    if not menu:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="menu not found")
    return MenuResponse(**menu)


@router.post(
    path="/",
    response_model=MenuResponse,
    summary="Create a menu",
    tags=["menus"]
)
async def menu_create(
        menu: MenuCreate
) -> MenuResponse:
    menu: dict = dict()
    return MenuResponse(**menu)


@router.patch(
    path="/{menu_id}",
    response_model=MenuResponse,
    summary="Update a menu",
    tags=["menus"]
)
async def menu_update(
        menu_id: int,
        new_data: MenuUpdate
) -> MenuResponse:
    menu: Optional[dict] = dict()
    if not menu:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="menu not found")
    return MenuResponse(**menu)


@router.delete(
    path="/{menu_id",
    summary="Delete a menu",
    tags=["menus"]
)
async def menu_delete(
        menu_id: int
) -> dict:
    menu: Optional[dict] = dict()
    if not menu:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="menu not found")
    return {"status": True, "message": "The menu has been deleted"}
