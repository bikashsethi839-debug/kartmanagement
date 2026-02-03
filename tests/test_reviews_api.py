from app import app
from database.complaintstable import init_db


def test_create_and_list_review():
    init_db()
    client = app.test_client()
    rv = client.get('/api/products')
    pid = rv.get_json()['data'][0]['id']

    # create review
    rv = client.post(f'/api/reviews/product/{pid}', json={'author':'Alice','rating':5,'comment':'Great!'})
    assert rv.status_code == 201
    created = rv.get_json()['data']
    assert created['author'] == 'Alice'

    # list
    rv = client.get(f'/api/reviews/product/{pid}')
    assert rv.status_code == 200
    assert any(r['id'] == created['id'] for r in rv.get_json()['data'])
