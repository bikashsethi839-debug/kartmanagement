from app import app
from database.complaintstable import init_db


def test_cart_flow():
    init_db()
    client = app.test_client()
    # pick a product
    rv = client.get('/api/products')
    data = rv.get_json()['data']
    assert len(data) >= 1
    pid = data[0]['id']

    # add to cart
    rv = client.post('/api/cart', json={'product_id': pid, 'quantity': 2})
    assert rv.status_code == 201
    item = rv.get_json()['data']
    item_id = item['id']

    # get cart
    rv = client.get('/api/cart')
    assert rv.status_code == 200
    assert any(d['id'] == item_id for d in rv.get_json()['data'])

    # update quantity
    rv = client.put(f'/api/cart/{item_id}', json={'quantity': 3})
    assert rv.status_code == 200
    assert rv.get_json()['data']['quantity'] == 3

    # delete
    rv = client.delete(f'/api/cart/{item_id}')
    assert rv.status_code == 200
