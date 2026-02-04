from app import app
from database.complaintstable import init_db
from fastapi.testclient import TestClient


def test_products_endpoint():
    # Ensure DB exists and seeded
    init_db()
    client = TestClient(app)
    rv = client.get('/api/products')
    assert rv.status_code == 200
    json_data = rv.json()
    assert 'data' in json_data
    assert isinstance(json_data['data'], list)
