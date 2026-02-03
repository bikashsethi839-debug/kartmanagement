from database.connection import get_connection

class WishlistService:
    def list_all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT w.id, w.product_id, p.name, p.price FROM wishlist w JOIN products p ON p.id = w.product_id ORDER BY w.id DESC')
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def add(self, payload):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO wishlist (product_id) VALUES (?)', (payload.get('product_id'),))
        conn.commit()
        item_id = cur.lastrowid
        conn.close()
        return self.get(item_id)

    def get(self, item_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, product_id FROM wishlist WHERE id=?', (item_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    def delete(self, item_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM wishlist WHERE id=?', (item_id,))
        conn.commit()
        changed = cur.rowcount
        conn.close()
        return changed > 0
