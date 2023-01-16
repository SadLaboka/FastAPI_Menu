import json

import pytest
from fastapi import HTTPException


# from uuid import uuid4


class TestMenuRoutes:

    async def test_create_menu(self, client):
        menu_data = {
            "title": "Test menu",
            "description": "Test menu description"
        }
        resp = await client.post("/api/v1/menus/", data=json.dumps(menu_data))
        resp_data = resp.json()
        assert resp.status_code == 201
        assert resp_data["title"] == menu_data["title"]
        assert resp_data["description"] == menu_data["description"]
        assert resp_data["submenus_count"] == 0
        assert resp_data["dishes_count"] == 0

    async def test_get_menu_404(self, client, menu_data):
        wrong_id = menu_data["id_"]
        resp = await client.get(f"/api/v1/menus/{wrong_id}")
        resp_data = resp.json()
        assert resp.status_code == 404
        assert resp_data["detail"] == "menu not found"

    async def test_get_menu(self, client, menu_data, create_menu_in_database):
        await create_menu_in_database(**menu_data)
        resp = await client.get(f"/api/v1/menus/{menu_data['id_']}")
        assert resp.status_code == 200
        resp_data = resp.json()
        assert resp_data["id"] == menu_data["id_"]
        assert resp_data["title"] == menu_data["title"]
        assert resp_data["description"] == menu_data["description"]
        assert resp_data["submenus_count"] == 0
        assert resp_data["dishes_count"] == 0

    async def test_get_menu_list_empty(self, client):
        resp = await client.get("/api/v1/menus/")
        assert resp.status_code == 200
        resp_data = resp.json()
        assert resp_data == []

    async def test_get_menu_list(self, client, menu_data, create_menu_in_database):
        await create_menu_in_database(**menu_data)
        resp = await client.get("/api/v1/menus/")
        assert resp.status_code == 200
        resp_data = resp.json()
        assert isinstance(resp_data, list)
        data = resp_data[0]
        assert data["id"] == menu_data["id_"]
        assert data["title"] == menu_data["title"]
        assert data["description"] == menu_data["description"]
        assert data["submenus_count"] == 0
        assert data["dishes_count"] == 0

    async def test_update_menu_404(self, client, menu_data):
        new_data = {"title": "Updated title", "description": "Updated description"}
        resp = await client.patch(f"/api/v1/menus/{menu_data['id_']}", data=json.dumps(new_data))
        resp_data = resp.json()
        assert resp.status_code == 404
        assert resp_data["detail"] == "menu not found"

    async def test_update_menu(self, client, menu_data, create_menu_in_database):
        new_data = {"title": "Updated title", "description": "Updated description"}
        await create_menu_in_database(**menu_data)
        resp = await client.patch(f"/api/v1/menus/{menu_data['id_']}", data=json.dumps(new_data))
        resp_data = resp.json()
        assert resp_data["id"] == menu_data["id_"]
        assert resp_data["title"] == new_data["title"]
        assert resp_data["description"] == new_data["description"]
        assert resp_data["submenus_count"] == 0
        assert resp_data["dishes_count"] == 0

    async def test_delete_menu_404(self, client, menu_data):
        resp = await client.delete(f"/api/v1/menus/{menu_data['id_']}")
        resp_data = resp.json()
        assert resp.status_code == 404
        assert resp_data["detail"] == "menu not found"

    async def test_delete_menu(self, client, create_menu_in_database, menu_data):
        await create_menu_in_database(**menu_data)
        resp = await client.delete(f"/api/v1/menus/{menu_data['id_']}")
        assert resp.status_code == 200
        resp_data = resp.json()
        assert resp_data["status"] is True
        assert resp_data["message"] == "The menu has been deleted"

