from app import app
from database.complaintstable import init_db


def test_duplicate_and_bulk_delete():
    init_db()
    client = app.test_client()
    # create a product to duplicate
    rv = client.post('/api/products', json={'name':'DupKart','sku':'DK-1','price':10.0,'stock':1})
    assert rv.status_code == 201
    created = rv.get_json()['data']
    pid = created['id']

    # duplicate
    rv = client.post(f'/api/products/{pid}/duplicate')
    assert rv.status_code == 201
    dup = rv.get_json()['data']
    assert dup['name'].endswith('(Copy)')

    # bulk delete both
    rv = client.post('/api/products/bulk-delete', json={'ids':[pid, dup['id']]})
    assert rv.status_code == 200
    assert rv.get_json()['data']['deleted'] >= 1

    # make sure they are gone
    rv = client.get(f'/api/products/{pid}')
    assert rv.status_code == 404
