def test_create_subscription(client, auth_headers):
    response = client.post(
        "/subscriptions/",
        json={
            "name": "Netflix",
            "amount": 15.99,
            "currency": "USD",
            "period": "monthly",
            "next_billing_date": "2026-10-15",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Netflix"


def test_update_subscription(client, auth_headers):
    create_response = client.post(
        "/subscriptions/",
        json={"name": "Netflix", "amount": 15.99, "currency": "USD", "period": "monthly", "next_billing_date": "2026-10-15"},
        headers=auth_headers,
    )
    subscription_id = create_response.json()["id"]

    update_response = client.put(
        f"/subscriptions/{subscription_id}",
        json={"name": "Netflix Premium", "amount": 19.99, "currency": "USD", "period": "monthly", "next_billing_date": "2026-10-15"},
        headers=auth_headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["amount"] == 19.99


def test_get_nonexistent_subscription_returns_404(client, auth_headers):
    response = client.get("/subscriptions/99999", headers=auth_headers)
    assert response.status_code == 404