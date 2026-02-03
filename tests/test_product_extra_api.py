from app import app
from database.complaintstable import init_db


def test_duplicate_and_reviews():
    init_db()
    client = app.test_client()

    # create a product to duplicate
    rv = client.post('/api/products', json={'name':'Dup Kart','sku':'D-1','price':10.0,'stock':1,'description':'dup'})
    assert rv.status_code == 201
    pid = rv.get_json()['data']['id']

    # duplicate
    rv = client.post(f'/api/products/{pid}/duplicate')
    assert rv.status_code == 201
    new = rv.get_json()['data']
    assert new['name'].endswith('(copy)')

    # reviews
    rv = client.post(f'/api/products/{pid}/reviews', json={'author':'Bob','rating':4,'comment':'Good'})
    assert rv.status_code == 201
    rid = rv.get_json()['data']['id']

    rv = client.get(f'/api/products/{pid}/reviews')
    assert rv.status_code == 200
    found = rv.get_json()['data']
    assert any(r['id'] == rid for r in found)

    # bulk delete
    # create two products and then bulk delete
    a = client.post('/api/products', json={'name':'A','sku':'A','price':1,'stock':1,'description':''}).get_json()['data']['id']
    b = client.post('/api/products', json={'name':'B','sku':'B','price':2,'stock':2,'description':''}).get_json()['data']['id']
    rv = client.post('/api/products/bulk-delete', json={'ids':[a,b]})
    assert rv.status_code == 200
    assert rv.get_json()['data']['deleted_count'] >= 2
