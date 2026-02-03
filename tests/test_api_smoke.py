from app import app
from database.complaintstable import init_db


def test_products_endpoint():
    init_db()
    client = app.test_client()
    r = client.get('/api/products')
    assert r.status_code == 200
    data = r.get_json()
    assert 'data' in data


def test_create_product():
    client = app.test_client()
    payload = {'name':'Test','sku':'T-1','price':9.99,'stock':3}
    r = client.post('/api/products', json=payload)
    assert r.status_code == 201
    data = r.get_json()
    assert data['data']['name'] == 'Test'
