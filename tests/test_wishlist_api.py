from app import app
from database.complaintstable import init_db


def test_wishlist_flow():
    init_db()
    client = app.test_client()
    # add a product to wishlist
    rv = client.get('/api/products')
    pid = rv.get_json()['data'][0]['id']

    rv = client.post('/api/cart/wishlist', json={'product_id': pid})
    assert rv.status_code == 201
    item_id = rv.get_json()['data']['id']

    # list wishlist
    rv = client.get('/api/cart/wishlist')
    assert rv.status_code == 200
    assert any(i['id'] == item_id for i in rv.get_json()['data'])

    # delete
    rv = client.delete(f'/api/cart/wishlist/{item_id}')
    assert rv.status_code == 200
