from app import app
from database.complaintstable import init_db


def test_review_delete():
    init_db()
    client = app.test_client()
    rv = client.post('/api/products', json={'name':'Rtest','sku':'R-1','price':1,'stock':1,'description':''})
    pid = rv.get_json()['data']['id']
    rv = client.post(f'/api/products/{pid}/reviews', json={'author':'X','rating':5,'comment':'ok'})
    rid = rv.get_json()['data']['id']

    rv = client.delete(f'/api/products/{pid}/reviews/{rid}')
    assert rv.status_code == 200
    # ensure not found after delete
    rv = client.delete(f'/api/products/{pid}/reviews/{rid}')
    assert rv.status_code == 404
