import json
import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_add_to_cart(client):
    response = client.post('/api/cart', json={'name': 'Laptop', 'qty': 2})
    assert response.status_code == 201
    data = response.get_json()
    assert data['item']['name'] == 'Laptop'
    assert data['item']['qty'] == 2


def test_get_cart(client):
    # Add an item first
    client.post('/api/cart', json={'name': 'Mouse', 'qty': 1})
    response = client.get('/api/cart')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data['cart'], list)
    assert len(data['cart']) > 0


def test_update_cart_item(client):
    # Add item first
    client.post('/api/cart', json={'name': 'Keyboard', 'qty': 1})
    response = client.put('/api/cart/1', json={'qty': 5})
    assert response.status_code == 200
    data = response.get_json()
    assert data['item']['qty'] == 5


def test_delete_cart_item(client):
    # Add item first
    client.post('/api/cart', json={'name': 'Monitor', 'qty': 1})
    response = client.delete('/api/cart/1')
    assert response.status_code == 200
    data = response.get_json()
    assert "deleted" in data['message']
