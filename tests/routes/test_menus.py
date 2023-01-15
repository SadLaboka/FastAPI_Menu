import json
from uuid import uuid4


class TestMenuRoutes:

    async def test_create_menu(self, client):
        menu_data = {
            "title": "Test menu",
            "description": "Test menu description"
        }
        resp = client.post("/api/v1/menus/", data=json.dumps(menu_data))
        resp_data = resp.json()
        assert resp.status_code == 201
        assert resp_data["title"] == menu_data["title"]
        assert resp_data["description"] == menu_data["description"]
        assert resp_data["submenus_count"] == 0
        assert resp_data["dishes_count"] == 0

    # async def test_delete_menu(self, client, create_menu_in_database):
    #     menu_data = {
    #         "id_": "4468bbfd-e02e-4936-9e25-402520dcecf2",
    #         "title": "Test menu",
    #         "description": "Test menu description"
    #     }
    #     await create_menu_in_database(**menu_data)
    #     resp = client.delete(f"/api/v1/menus/{menu_data['id_']}")
    #     assert resp.code == 200
    #     resp_data = resp.json()
    #     assert resp_data["status"] is True
    #     assert resp_data["message"] == "The menu has been deleted"
