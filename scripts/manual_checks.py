from app import app
from database.complaintstable import init_db
import json

init_db()
client = app.test_client()

checks = []

def run(name, fn):
    try:
        res = fn()
        checks.append((name, True, res))
        print(f"[OK] {name} -> {res}")
    except Exception as e:
        checks.append((name, False, str(e)))
        print(f"[FAIL] {name} -> {e}")

# Pages/static
run('GET /', lambda: client.get('/').status_code)
run('GET /catalog.html', lambda: client.get('/catalog.html').status_code)
run('GET /assets/css/style.css', lambda: client.get('/assets/css/style.css').status_code)

# API products
rv = client.get('/api/products')
run('GET /api/products', lambda: rv.status_code if rv else None)
products = rv.get_json()['data']
print('Products count:', len(products))

# Create product
payload = {'name':'ManualTest','sku':'MAN-1','price':42.0,'stock':3,'description':'manual'}
rv = client.post('/api/products', json=payload)
run('POST /api/products', lambda: rv.status_code)
created = rv.get_json()['data']
new_id = created['id']

# Read created
rv = client.get(f'/api/products/{new_id}')
run('GET /api/products/:id', lambda: rv.status_code)

# Update
rv = client.put(f'/api/products/{new_id}', json={'name':'ManualTest2','sku':'MAN-1','price':50,'stock':4,'description':'u'})
run('PUT /api/products/:id', lambda: rv.status_code)

# Duplicate
rv = client.post(f'/api/products/{new_id}/duplicate')
run('POST /api/products/:id/duplicate', lambda: rv.status_code)

# Bulk delete
# create two
a = client.post('/api/products', json={'name':'A','sku':'A1','price':1,'stock':1}).get_json()['data']['id']
b = client.post('/api/products', json={'name':'B','sku':'B1','price':2,'stock':2}).get_json()['data']['id']
rv = client.post('/api/products/bulk-delete', json={'ids':[a,b]})
run('POST /api/products/bulk-delete', lambda: rv.status_code)

# Reviews
rv = client.post(f'/api/products/{new_id}/reviews', json={'author':'T','rating':5,'comment':'ok'})
run('POST review', lambda: rv.status_code)
rid = rv.get_json()['data']['id']
rv = client.get(f'/api/products/{new_id}/reviews')
run('GET reviews', lambda: rv.status_code)

rv = client.delete(f'/api/products/{new_id}/reviews/{rid}')
run('DELETE review', lambda: rv.status_code)

# Cart
rv = client.post('/api/cart', json={'product_id': new_id, 'quantity': 2})
run('POST /api/cart', lambda: rv.status_code)
item_id = rv.get_json()['data']['id']
rv = client.get('/api/cart')
run('GET /api/cart', lambda: rv.status_code)
rv = client.put(f'/api/cart/{item_id}', json={'quantity':3})
run('PUT /api/cart/:id', lambda: rv.status_code)
rv = client.delete(f'/api/cart/{item_id}')
run('DELETE /api/cart/:id', lambda: rv.status_code)

# Wishlist
rv = client.post('/api/cart/wishlist', json={'product_id': new_id})
run('POST /api/cart/wishlist', lambda: rv.status_code)
ws_id = rv.get_json()['data']['id']
rv = client.get('/api/cart/wishlist')
run('GET /api/cart/wishlist', lambda: rv.status_code)
rv = client.delete(f'/api/cart/wishlist/{ws_id}')
run('DELETE /api/cart/wishlist/:id', lambda: rv.status_code)

print('\nSummary:')
for name, ok, info in checks:
    print(f" - {name}: {'OK' if ok else 'FAIL'} -> {info}")
