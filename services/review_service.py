from database.connection import get_connection

class ReviewService:
    def list_for_product(self, product_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM reviews WHERE product_id=? ORDER BY id DESC', (product_id,))
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def create(self, product_id, payload):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO reviews (product_id, author, rating, comment) VALUES (?, ?, ?, ?)',
                    (product_id, payload.get('author', 'Anon'), payload.get('rating', 5), payload.get('comment')))
        conn.commit()
        review_id = cur.lastrowid
        conn.close()
        return self.get(review_id)

    def get(self, review_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM reviews WHERE id=?', (review_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    def delete(self, review_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM reviews WHERE id=?', (review_id,))
        conn.commit()
        changed = cur.rowcount
        conn.close()
        return changed > 0
