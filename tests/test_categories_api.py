def test_create_category(client, auth_headers):
    response = client.post("/categories/", json={"name": "Еда"}, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["name"] == "Еда"


def test_list_categories(client, auth_headers):
    client.post("/categories/", json={"name": "Еда"}, headers=auth_headers)
    client.post("/categories/", json={"name": "Транспорт"}, headers=auth_headers)

    response = client.get("/categories/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_delete_category(client, auth_headers):
    create_response = client.post("/categories/", json={"name": "Еда"}, headers=auth_headers)
    category_id = create_response.json()["id"]

    delete_response = client.delete(f"/categories/{category_id}", headers=auth_headers)
    assert delete_response.status_code == 204

    list_response = client.get("/categories/", headers=auth_headers)
    assert len(list_response.json()) == 0