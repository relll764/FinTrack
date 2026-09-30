def test_create_account(client, auth_headers):
    response = client.post(
        "/accounts/",
        json={"name": "Карта", "balance": 1000.0, "currency": "USD", "description": None},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["balance"] == 1000.0
    assert data["currency"] == "USD"


def test_cannot_create_duplicate_account_name_for_same_user(client, auth_headers):
    client.post("/accounts/", json={"name": "Карта", "balance": 1000.0, "currency": "USD", "description": None}, headers=auth_headers)
    second = client.post("/accounts/", json={"name": "Карта", "balance": 500.0, "currency": "USD", "description": None}, headers=auth_headers)
    assert second.status_code == 400


def test_get_nonexistent_account_returns_404(client, auth_headers):
    response = client.get("/accounts/99999", headers=auth_headers)
    assert response.status_code == 404


def test_cannot_see_other_users_account(client, auth_headers):
    create_response = client.post(
        "/accounts/", json={"name": "Карта", "balance": 1000.0, "currency": "USD", "description": None}, headers=auth_headers
    )
    account_id = create_response.json()["id"]

    client.post("/auth/register", json={"email": "other2@test.com", "username": "otheruser2", "password": "testpass123"})
    login_response = client.post("/auth/login", json={"email": "other2@test.com", "password": "testpass123"})
    other_headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}

    response = client.get(f"/accounts/{account_id}", headers=other_headers)
    assert response.status_code == 404


def test_update_account(client, auth_headers, make_account):
    account_id = make_account(balance=1000.0)

    response = client.put(
        f"/accounts/{account_id}",
        json={"name": "Карта обновлённая", "balance": 1500.0, "currency": "USD", "description": None},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["balance"] == 1500.0


def test_delete_account(client, auth_headers, make_account):
    account_id = make_account()

    response = client.delete(f"/accounts/{account_id}", headers=auth_headers)
    assert response.status_code == 204

    list_response = client.get("/accounts/", headers=auth_headers)
    assert len(list_response.json()) == 0