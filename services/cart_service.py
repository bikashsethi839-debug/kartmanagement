from database.connection import get_connection

class CartService:
    def list_all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT cart.id, product_id, quantity, p.name, p.price FROM cart JOIN products p ON p.id = cart.product_id')
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def add(self, payload):
        product_id = payload.get('product_id')
        qty = payload.get('quantity', 1)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO cart (product_id, quantity) VALUES (?, ?)', (product_id, qty))
        conn.commit()
        item_id = cur.lastrowid
        conn.close()
        return self.get(item_id)

    def get(self, item_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, product_id, quantity FROM cart WHERE id=?', (item_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    def update(self, item_id, payload):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('UPDATE cart SET quantity=? WHERE id=?', (payload.get('quantity'), item_id))
        conn.commit()
        changed = cur.rowcount
        conn.close()
        return self.get(item_id) if changed else None

    def delete(self, item_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM cart WHERE id=?', (item_id,))
        conn.commit()
        changed = cur.rowcount
        conn.close()
        return changed > 0
