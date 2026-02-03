from app import app
from database.complaintstable import init_db


def test_create_product():
    init_db()
    client = app.test_client()
    payload = {
        'name': 'Test Kart',
        'sku': 'TK-999',
        'price': 123.45,
        'stock': 7,
        'description': 'A test kart'
    }
    rv = client.post('/api/products', json=payload)
    assert rv.status_code == 201
    data = rv.get_json()
    assert data['status'] == 'created'
    created = data['data']
    # fetch it
    rv = client.get(f"/api/products/{created['id']}")
    assert rv.status_code == 200
    got = rv.get_json()['data']
    assert got['name'] == payload['name']
    assert got['sku'] == payload['sku']
    assert float(got['price']) == payload['price']
