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

from unittest.mock import patch


def test_create_expense_with_account_deducts_balance(client, auth_headers, make_category, make_account):
    category_id = make_category()
    account_id = make_account(balance=1000.0, currency="USD")

    with patch("app.api.routes.expenses.convert", return_value=100.0):
        response = client.post(
            "/expenses/",
            json={
                "amount": 100.0, "currency": "USD", "description": None,
                "date": "2026-09-20", "category_id": category_id, "account_id": account_id
            },
            headers=auth_headers,
        )
    assert response.status_code == 201

    account_response = client.get(f"/accounts/{account_id}", headers=auth_headers)
    assert account_response.json()["balance"] == 900.0


def test_delete_expense_refunds_account_balance(client, auth_headers, make_category, make_account):
    category_id = make_category()
    account_id = make_account(balance=1000.0, currency="USD")

    with patch("app.api.routes.expenses.convert", return_value=100.0):
        create_response = client.post(
            "/expenses/",
            json={
                "amount": 100.0, "currency": "USD", "description": None,
                "date": "2026-09-20", "category_id": category_id, "account_id": account_id
            },
            headers=auth_headers,
        )
    expense_id = create_response.json()["id"]

    client.delete(f"/expenses/{expense_id}", headers=auth_headers)

    account_response = client.get(f"/accounts/{account_id}", headers=auth_headers)
    assert account_response.json()["balance"] == 1000.0


def test_update_expense_amount_adjusts_account_balance(client, auth_headers, make_category, make_account):
    category_id = make_category()
    account_id = make_account(balance=1000.0, currency="USD")

    with patch("app.api.routes.expenses.convert", return_value=100.0):
        create_response = client.post(
            "/expenses/",
            json={
                "amount": 100.0, "currency": "USD", "description": None,
                "date": "2026-09-20", "category_id": category_id, "account_id": account_id
            },
            headers=auth_headers,
        )
    expense_id = create_response.json()["id"]

    with patch("app.api.routes.expenses.convert", return_value=200.0):
        client.put(
            f"/expenses/{expense_id}",
            json={
                "amount": 200.0, "currency": "USD", "description": None,
                "date": "2026-09-20", "category_id": category_id, "account_id": account_id
            },
            headers=auth_headers,
        )

    account_response = client.get(f"/accounts/{account_id}", headers=auth_headers)
    assert account_response.json()["balance"] == 800.0


def test_create_expense_without_account_does_not_touch_any_balance(client, auth_headers, make_category, make_account):
    category_id = make_category()
    account_id = make_account(balance=1000.0, currency="USD")

    client.post(
        "/expenses/",
        json={
            "amount": 50.0, "currency": "USD", "description": None,
            "date": "2026-09-20", "category_id": category_id, "account_id": None
        },
        headers=auth_headers,
    )

    account_response = client.get(f"/accounts/{account_id}", headers=auth_headers)
    assert account_response.json()["balance"] == 1000.0