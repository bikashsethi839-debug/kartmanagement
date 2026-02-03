from database.connection import get_connection

class ProductService:
    def list_all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM products ORDER BY id DESC')
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def get(self, product_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    def create(self, payload):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO products (name, sku, price, stock, description) VALUES (?, ?, ?, ?, ?)',
                    (payload.get('name'), payload.get('sku'), payload.get('price', 0.0), payload.get('stock', 0), payload.get('description')))
        conn.commit()
        product_id = cur.lastrowid
        conn.close()
        return self.get(product_id)

    def update(self, product_id, payload):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('UPDATE products SET name=?, sku=?, price=?, stock=?, description=? WHERE id=?',
                    (payload.get('name'), payload.get('sku'), payload.get('price'), payload.get('stock'), payload.get('description'), product_id))
        conn.commit()
        changed = cur.rowcount
        conn.close()
        return self.get(product_id) if changed else None

    def delete(self, product_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM products WHERE id=?', (product_id,))
        conn.commit()
        changed = cur.rowcount
        conn.close()
        return changed > 0
