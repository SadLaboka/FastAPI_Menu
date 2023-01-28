import json


class TestMenuRoutes:

    async def test_create_menu(self, client):
        menu_data = {
            "title": "Test menu",
            "description": "Test menu description",
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

    async def test_get_menu(
        self,
        client,
        menu_data,
        submenu_data,
        dish_data,
        create_menu_in_database,
        create_submenu_in_database,
        create_dish_in_database,
    ):
        await create_menu_in_database(**menu_data)
        resp = await client.get(f"/api/v1/menus/{menu_data['id_']}")
        assert resp.status_code == 200
        resp_data = resp.json()
        assert resp_data["id"] == menu_data["id_"]
        assert resp_data["title"] == menu_data["title"]
        assert resp_data["description"] == menu_data["description"]
        assert resp_data["submenus_count"] == 0
        assert resp_data["dishes_count"] == 0

        await create_submenu_in_database(**submenu_data)
        resp = await client.get(f"/api/v1/menus/{menu_data['id_']}")
        resp_data = resp.json()
        assert resp_data["submenus_count"] == 1
        assert resp_data["dishes_count"] == 0

        await create_dish_in_database(**dish_data)
        resp = await client.get(f"/api/v1/menus/{menu_data['id_']}")
        resp_data = resp.json()
        assert resp_data["dishes_count"] == 1

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


class TestSubMenuRoutes:

    async def test_create_submenu(
        self,
        client,
        menu_data,
        submenu_data,
        create_menu_in_database,
    ):
        await create_menu_in_database(**menu_data)
        resp = await client.post(
            f"/api/v1/menus/{menu_data['id_']}/submenus",
            data=json.dumps(submenu_data),
        )
        resp_data = resp.json()
        assert resp.status_code == 201
        assert resp_data["title"] == submenu_data["title"]
        assert resp_data["description"] == submenu_data["description"]
        assert resp_data["dishes_count"] == 0

    async def test_create_submenu_404(
        self,
        client,
        menu_data,
        submenu_data,
    ):
        resp = await client.post(
            f"/api/v1/menus/{menu_data['id_']}/submenus",
            data=json.dumps(submenu_data),
        )
        assert resp.status_code == 404
        resp_data = resp.json()
        assert resp_data["detail"] == "menu not found"

    async def test_get_submenu_404(self, client, menu_data, submenu_data, create_menu_in_database):
        await create_menu_in_database(**menu_data)
        resp = await client.get(f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}")
        resp_data = resp.json()
        assert resp.status_code == 404
        assert resp_data["detail"] == "submenu not found"

    async def test_get_submenu(
        self,
        client,
        menu_data,
        submenu_data,
        dish_data,
        create_menu_in_database,
        create_submenu_in_database,
        create_dish_in_database,
    ):
        await create_menu_in_database(**menu_data)
        await create_submenu_in_database(**submenu_data)
        resp = await client.get(f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}")
        assert resp.status_code == 200
        resp_data = resp.json()
        assert resp_data["id"] == submenu_data["id_"]
        assert resp_data["title"] == submenu_data["title"]
        assert resp_data["description"] == submenu_data["description"]
        assert resp_data["dishes_count"] == 0

        await create_dish_in_database(**dish_data)
        resp = await client.get(f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}")
        resp_data = resp.json()
        assert resp_data["dishes_count"] == 1

    async def test_get_submenu_list_empty(self, client, menu_data, create_menu_in_database):
        await create_menu_in_database(**menu_data)
        resp = await client.get(f"/api/v1/menus/{menu_data['id_']}/submenus")
        assert resp.status_code == 200
        resp_data = resp.json()
        assert resp_data == []

    async def test_get_submenu_list(
        self,
        client,
        menu_data,
        submenu_data,
        create_menu_in_database,
        create_submenu_in_database,
    ):
        await create_menu_in_database(**menu_data)
        await create_submenu_in_database(**submenu_data)
        resp = await client.get(f"/api/v1/menus/{menu_data['id_']}/submenus")
        assert resp.status_code == 200
        resp_data = resp.json()
        assert isinstance(resp_data, list)
        data = resp_data[0]
        assert data["id"] == submenu_data["id_"]
        assert data["title"] == submenu_data["title"]
        assert data["description"] == submenu_data["description"]
        assert data["dishes_count"] == 0

    async def test_update_menu_404(self, client, menu_data, submenu_data, create_menu_in_database):
        await create_menu_in_database(**menu_data)
        new_data = {"title": "Updated title", "description": "Updated description"}
        resp = await client.patch(
            f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}",
            data=json.dumps(new_data),
        )
        resp_data = resp.json()
        assert resp.status_code == 404
        assert resp_data["detail"] == "submenu not found"

    async def test_update_submenu(
        self,
        client,
        menu_data,
        submenu_data,
        create_menu_in_database,
        create_submenu_in_database,
    ):
        new_data = {"title": "Updated title", "description": "Updated description"}
        await create_menu_in_database(**menu_data)
        await create_submenu_in_database(**submenu_data)
        resp = await client.patch(
            f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}",
            data=json.dumps(new_data),
        )
        resp_data = resp.json()
        assert resp_data["id"] == submenu_data["id_"]
        assert resp_data["title"] == new_data["title"]
        assert resp_data["description"] == new_data["description"]
        assert resp_data["dishes_count"] == 0

    async def test_delete_dish_404(self, client, menu_data, submenu_data):
        resp = await client.delete(f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}")
        resp_data = resp.json()
        assert resp.status_code == 404
        assert resp_data["detail"] == "submenu not found"

    async def test_delete_dish(
        self,
        client,
        menu_data,
        submenu_data,
        create_menu_in_database,
        create_submenu_in_database,
    ):
        await create_menu_in_database(**menu_data)
        await create_submenu_in_database(**submenu_data)
        resp = await client.delete(f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}")
        assert resp.status_code == 200
        resp_data = resp.json()
        assert resp_data["status"] is True
        assert resp_data["message"] == "The submenu has been deleted"


class TestDishRoutes:

    async def test_create_dish(
        self,
        client,
        menu_data,
        submenu_data,
        dish_data,
        create_menu_in_database,
        create_submenu_in_database,
    ):
        await create_menu_in_database(**menu_data)
        await create_submenu_in_database(**submenu_data)
        resp = await client.post(
            f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}/dishes",
            data=json.dumps(dish_data),
        )
        resp_data = resp.json()
        assert resp.status_code == 201
        assert resp_data["title"] == dish_data["title"]
        assert resp_data["description"] == dish_data["description"]
        assert resp_data["price"] == str(dish_data["price"])

    async def test_create_dish_404(
        self,
        client,
        menu_data,
        submenu_data,
        dish_data,
    ):
        resp = await client.post(
            f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}/dishes",
            data=json.dumps(dish_data),
        )
        assert resp.status_code == 404
        resp_data = resp.json()
        assert resp_data["detail"] == "dish not found"

    async def test_get_dish_404(
        self,
        client,
        menu_data,
        submenu_data,
        dish_data,
        create_menu_in_database,
        create_submenu_in_database,
    ):
        await create_menu_in_database(**menu_data)
        resp = await client.get(
            f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}/dishes/{dish_data['id_']}",
        )
        resp_data = resp.json()
        assert resp.status_code == 404
        assert resp_data["detail"] == "dish not found"

    async def test_get_dish(
        self,
        client,
        menu_data,
        submenu_data,
        dish_data,
        create_menu_in_database,
        create_submenu_in_database,
        create_dish_in_database,
    ):
        await create_menu_in_database(**menu_data)
        await create_submenu_in_database(**submenu_data)
        await create_dish_in_database(**dish_data)
        resp = await client.get(
            f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}/dishes/{dish_data['id_']}",
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        assert resp_data["id"] == dish_data["id_"]
        assert resp_data["title"] == dish_data["title"]
        assert resp_data["description"] == dish_data["description"]
        assert resp_data["price"] == str(dish_data["price"])

    async def test_get_dish_list_empty(
        self,
        client,
        menu_data,
        submenu_data,
        create_menu_in_database,
        create_submenu_in_database,
    ):
        await create_menu_in_database(**menu_data)
        await create_submenu_in_database(**submenu_data)
        resp = await client.get(f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}/dishes")
        assert resp.status_code == 200
        resp_data = resp.json()
        assert resp_data == []

    #
    async def test_get_dish_list(
        self,
        client,
        menu_data,
        submenu_data,
        dish_data,
        create_menu_in_database,
        create_submenu_in_database,
        create_dish_in_database,
    ):
        await create_menu_in_database(**menu_data)
        await create_submenu_in_database(**submenu_data)
        await create_dish_in_database(**dish_data)
        resp = await client.get(f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}/dishes")
        assert resp.status_code == 200
        resp_data = resp.json()
        assert isinstance(resp_data, list)
        data = resp_data[0]
        assert data["id"] == dish_data["id_"]
        assert data["title"] == dish_data["title"]
        assert data["description"] == dish_data["description"]
        assert data["price"] == str(dish_data["price"])

    async def test_update_dish_404(
        self,
        client,
        menu_data,
        submenu_data,
        dish_data,
        create_menu_in_database,
        create_submenu_in_database,
    ):
        await create_menu_in_database(**menu_data)
        await create_submenu_in_database(**submenu_data)
        new_data = {"title": "Updated title", "description": "Updated description", "price": 12.2}
        resp = await client.patch(
            f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}/dishes/{dish_data['id_']}",
            data=json.dumps(new_data),
        )
        resp_data = resp.json()
        assert resp.status_code == 404
        assert resp_data["detail"] == "dish not found"

    async def test_update_dish(
        self,
        client,
        menu_data,
        submenu_data,
        dish_data,
        create_menu_in_database,
        create_submenu_in_database,
        create_dish_in_database,
    ):
        new_data = {"title": "Updated title", "description": "Updated description", "price": 12.2}
        await create_menu_in_database(**menu_data)
        await create_submenu_in_database(**submenu_data)
        await create_dish_in_database(**dish_data)
        resp = await client.patch(
            f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}/dishes/{dish_data['id_']}",
            data=json.dumps(new_data),
        )
        resp_data = resp.json()
        assert resp_data["id"] == dish_data["id_"]
        assert resp_data["title"] == new_data["title"]
        assert resp_data["description"] == new_data["description"]

    async def test_delete_dish_404(self, client, menu_data, submenu_data, dish_data):
        resp = await client.delete(
            f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}/dishes/{dish_data['id_']}",
        )
        resp_data = resp.json()
        assert resp.status_code == 404
        assert resp_data["detail"] == "dish not found"

    async def test_delete_dish(
        self,
        client,
        menu_data,
        submenu_data,
        dish_data,
        create_menu_in_database,
        create_submenu_in_database,
        create_dish_in_database,
    ):
        await create_menu_in_database(**menu_data)
        await create_submenu_in_database(**submenu_data)
        await create_dish_in_database(**dish_data)
        resp = await client.delete(
            f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}/dishes/{dish_data['id_']}",
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        assert resp_data["status"] is True
        assert resp_data["message"] == "The dish has been deleted"


class TestCascadeDelete:

    async def test_cascade_delete_dishes(
        self,
        client,
        menu_data,
        submenu_data,
        dish_data,
        create_menu_in_database,
        create_submenu_in_database,
        create_dish_in_database,
        delete_menu_from_database,
        delete_submenu_from_database,
    ):
        await create_menu_in_database(**menu_data)
        await create_submenu_in_database(**submenu_data)
        await create_dish_in_database(**dish_data)

        resp = await client.get(
            f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}/dishes/{dish_data['id_']}",
        )
        assert resp.status_code == 200

        await delete_submenu_from_database(submenu_data['id_'])
        await create_submenu_in_database(**submenu_data)
        resp = await client.get(
            f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}/dishes/{dish_data['id_']}",
        )
        assert resp.status_code == 404

    async def test_cascade_delete_submenus(
        self,
        client,
        menu_data,
        submenu_data,
        create_menu_in_database,
        create_submenu_in_database,
        delete_menu_from_database,
        delete_submenu_from_database,
    ):
        await create_menu_in_database(**menu_data)
        await create_submenu_in_database(**submenu_data)

        resp = await client.get(
            f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}",
        )
        assert resp.status_code == 200

        await delete_menu_from_database(menu_data['id_'])
        await create_menu_in_database(**menu_data)
        resp = await client.get(
            f"/api/v1/menus/{menu_data['id_']}/submenus/{submenu_data['id_']}",
        )
        assert resp.status_code == 404
