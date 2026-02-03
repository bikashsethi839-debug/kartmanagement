from app import app
from database.complaintstable import init_db


def test_update_product():
    init_db()
    client = app.test_client()

    rv = client.post('/api/products', json={'name':'Up Kart','sku':'UP-1','price':9.99,'stock':3,'description':'up'})
    assert rv.status_code == 201
    pid = rv.get_json()['data']['id']

    rv = client.put(f'/api/products/{pid}', json={'name':'Updated','sku':'UP-1','price':19.99,'stock':5,'description':'updated'})
    assert rv.status_code == 200
    got = rv.get_json()['data']
    assert got['name'] == 'Updated'
    assert float(got['price']) == 19.99
    assert got['stock'] == 5
