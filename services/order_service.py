from database.connection import get_connection

class OrderService:
    def list_all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT o.*, c.name as customer_name, c.email as customer_email
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            ORDER BY o.created_at DESC
        """)
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get(self, order_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT o.*, c.name as customer_name, c.email as customer_email
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            WHERE o.id = ?
        """, (order_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_order_items(self, order_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_customer_orders(self, customer_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders WHERE customer_id = ? ORDER BY created_at DESC", (customer_id,))
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def create(self, data):
        conn = get_connection()
        cur = conn.cursor()
        
        # Create order
        cur.execute(
            "INSERT INTO orders (customer_id, total_amount, status) VALUES (?, ?, ?)",
            (data.get('customer_id'), data.get('total_amount', 0), data.get('status', 'Pending'))
        )
        order_id = cur.lastrowid
        
        # Add order items
        items = data.get('items', [])
        for item in items:
            cur.execute(
                "INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES (?, ?, ?, ?, ?)",
                (order_id, item.get('product_id'), item.get('product_name'), item.get('quantity'), item.get('price'))
            )
        
        conn.commit()
        conn.close()
        return self.get(order_id)

    def update_status(self, order_id, status):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
        conn.commit()
        conn.close()
        return self.get(order_id)

    def delete(self, order_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
        cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        conn.commit()
        deleted = cur.rowcount > 0
        conn.close()
        return deleted
