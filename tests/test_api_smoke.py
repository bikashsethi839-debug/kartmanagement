from app import app
from database.complaintstable import init_db


def test_products_endpoint():
    # Ensure DB exists and seeded
    init_db()
    client = app.test_client()
    rv = client.get('/api/products')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert 'data' in json_data
    assert isinstance(json_data['data'], list)
