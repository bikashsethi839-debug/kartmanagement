from app import app
from database.complaintstable import init_db


def test_update_and_delete_product():
    init_db()
    client = app.test_client()
    rv = client.post('/api/products', json={'name':'UpdKart','sku':'UK-1','price':20.0,'stock':2})
    assert rv.status_code == 201
    pid = rv.get_json()['data']['id']

    # update
    rv = client.put(f'/api/products/{pid}', json={'name':'UpdKart2','sku':'UK-1','price':25.0,'stock':3})
    assert rv.status_code == 200
    got = rv.get_json()['data']
    assert got['name'] == 'UpdKart2'
    assert float(got['price']) == 25.0

    # delete
    rv = client.delete(f'/api/products/{pid}')
    assert rv.status_code == 200
    # confirm gone
    rv = client.get(f'/api/products/{pid}')
    assert rv.status_code == 404
