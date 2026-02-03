import sqlite3
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
        try:
            cur.execute('INSERT INTO products (name, sku, price, stock, description) VALUES (?, ?, ?, ?, ?)',
                        (payload.get('name'), payload.get('sku'), payload.get('price', 0.0), payload.get('stock', 0), payload.get('description')))
            conn.commit()
            product_id = cur.lastrowid
            conn.close()
            return self.get(product_id)
        except sqlite3.IntegrityError as e:
            conn.rollback()
            # Fail explicitly on unique constraint rather than silently removing sku
            if 'UNIQUE' in str(e).upper():
                raise
            raise

    def update(self, product_id, payload):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute('UPDATE products SET name=?, sku=?, price=?, stock=?, description=? WHERE id=?',
                        (payload.get('name'), payload.get('sku'), payload.get('price'), payload.get('stock'), payload.get('description'), product_id))
            conn.commit()
            changed = cur.rowcount
            conn.close()
            return self.get(product_id) if changed else None
        except sqlite3.IntegrityError as e:
            conn.rollback()
            if 'UNIQUE' in str(e).upper():
                # revert change and signal error
                raise
            raise

    def delete(self, product_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM products WHERE id=?', (product_id,))
        conn.commit()
        changed = cur.rowcount
        conn.close()
        return changed > 0

    def duplicate(self, product_id):
        # create a new product by copying fields
        src = self.get(product_id)
        if not src:
            return None
        payload = {
            'name': src.get('name') + ' (copy)',
            'sku': None,
            'price': src.get('price'),
            'stock': src.get('stock'),
            'description': src.get('description')
        }
        return self.create(payload)

    def bulk_delete(self, ids):
        conn = get_connection()
        cur = conn.cursor()
        cur.executemany('DELETE FROM products WHERE id=?', [(i,) for i in ids])
        conn.commit()
        deleted = conn.total_changes
        conn.close()
        return deleted
