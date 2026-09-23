def test_budget_status_no_expenses(client, auth_headers):
    category_response = client.post("/categories/", json={"name": "Еда"}, headers=auth_headers)
    category_id = category_response.json()["id"]

    budget_response = client.post(
        "/budgets/", json={"category_id": category_id, "monthly_limit": 100}, headers=auth_headers
    )
    budget_id = budget_response.json()["id"]

    status_response = client.get(f"/budgets/{budget_id}/status", headers=auth_headers)
    data = status_response.json()
    assert data["spent"] == 0
    assert data["exceeded"] is False


def test_budget_status_exceeded(client, auth_headers):
    category_response = client.post("/categories/", json={"name": "Еда"}, headers=auth_headers)
    category_id = category_response.json()["id"]

    budget_response = client.post(
        "/budgets/", json={"category_id": category_id, "monthly_limit": 100}, headers=auth_headers
    )
    budget_id = budget_response.json()["id"]

    # создаём расходы на общую сумму 150, превышая лимит в 100
    client.post(
        "/expenses/",
        json={"amount": 100, "currency": "USD", "description": None, "date": "2026-09-20", "category_id": category_id},
        headers=auth_headers,
    )
    client.post(
        "/expenses/",
        json={"amount": 50, "currency": "USD", "description": None, "date": "2026-09-21", "category_id": category_id},
        headers=auth_headers,
    )

    status_response = client.get(f"/budgets/{budget_id}/status", headers=auth_headers)
    data = status_response.json()
    assert data["spent"] == 150
    assert data["exceeded"] is True


def test_cannot_create_duplicate_budget_for_same_category(client, auth_headers):
    category_response = client.post("/categories/", json={"name": "Еда"}, headers=auth_headers)
    category_id = category_response.json()["id"]

    client.post("/budgets/", json={"category_id": category_id, "monthly_limit": 100}, headers=auth_headers)
    second_response = client.post("/budgets/", json={"category_id": category_id, "monthly_limit": 200}, headers=auth_headers)

    assert second_response.status_code == 400