from fastapi.testclient import TestClient
from app5 import app

client = TestClient(app)

def test_get_menu_success():
    response = client.get("/menu", params={"name": "Margherita"})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Margherita",
        "size": "Medium",
        "price": 8.99,
        "toppings": ["tomato sauce", "mozzarella", "basil"]
    }

def test_get_menu_not_found():
    response = client.get("/menu", params={"name": "Notthere"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Pizza 'Notthere' not found."}

def test_place_order_success():
    order = [{"id": 1, "quantity": 2}, {"id": 2, "quantity": 1}]
    response = client.post("/order", json=order)
    assert response.status_code == 200
    data = response.json()
    assert "order_id" in data
    assert "price" in data
    assert data["price"] == 27.97  # the normal maths is (2 * 8.99) + (1 * 9.99) = 27.97

def test_place_order_empty():
    response = client.post("/order", json=[])
    assert response.status_code == 400
    assert response.json() == {"detail": "Order is not given by the user."}

def test_place_order_invalid_item():
    order = [{"id": 90, "quantity": 1}]
    response = client.post("/order", json=order)
    assert response.status_code == 404
    assert response.json() == {"detail": "Pizza with ID 90 not found."}
