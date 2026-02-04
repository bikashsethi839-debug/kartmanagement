from app import app
from database.complaintstable import init_db
from fastapi.testclient import TestClient


def test_wishlist_flow():
    init_db()
    client = TestClient(app)
    # add a product to wishlist
    rv = client.get('/api/products')
    pid = rv.json()['data'][0]['id']

    rv = client.post('/api/cart/wishlist', json={'product_id': pid})
    assert rv.status_code == 201
    item_id = rv.json()['data']['id']

    # list wishlist
    rv = client.get('/api/cart/wishlist')
    assert rv.status_code == 200
    assert any(i['id'] == item_id for i in rv.json()['data'])

    # delete
    rv = client.delete(f'/api/cart/wishlist/{item_id}')
    assert rv.status_code == 200
