def test_create_expense(client, auth_headers):
    category_response = client.post("/categories/", json={"name": "Еда"}, headers=auth_headers)
    category_id = category_response.json()["id"]

    response = client.post(
        "/expenses/",
        json={"amount": 50.0, "currency": "USD", "description": None, "date": "2026-09-20", "category_id": category_id},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 50.0
    assert data["currency"] == "USD"


def test_get_nonexistent_expense_returns_404(client, auth_headers):
    response = client.get("/expenses/99999", headers=auth_headers)
    assert response.status_code == 404


def test_cannot_see_other_users_expense(client, auth_headers):
    category_response = client.post("/categories/", json={"name": "Еда"}, headers=auth_headers)
    category_id = category_response.json()["id"]

    create_response = client.post(
        "/expenses/",
        json={"amount": 30.0, "currency": "USD", "description": None, "date": "2026-09-20", "category_id": category_id},
        headers=auth_headers,
    )
    expense_id = create_response.json()["id"]

    client.post("/auth/register", json={"email": "other@test.com", "username": "otheruser", "password": "testpass123"})
    login_response = client.post("/auth/login", json={"email": "other@test.com", "password": "testpass123"})
    other_token = login_response.json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}

    response = client.get(f"/expenses/{expense_id}", headers=other_headers)
    assert response.status_code == 404