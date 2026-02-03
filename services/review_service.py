from database.connection import get_connection

class ReviewService:
    def list_for_product(self, product_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, product_id, author, rating, comment, created_at FROM reviews WHERE product_id=? ORDER BY created_at DESC', (product_id,))
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def create(self, product_id, payload):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO reviews (product_id, author, rating, comment) VALUES (?, ?, ?, ?)',
                    (product_id, payload.get('author', 'Anonymous'), payload.get('rating', 5), payload.get('comment')))
        conn.commit()
        rid = cur.lastrowid
        conn.close()
        return self.get(rid)

    def get(self, review_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, product_id, author, rating, comment, created_at FROM reviews WHERE id=?', (review_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None
