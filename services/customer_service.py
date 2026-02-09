from database.connection import get_connection

class CustomerService:
    def list_all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers ORDER BY created_at DESC")
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get(self, customer_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    def create(self, data):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO customers (name, email, phone, address) VALUES (?, ?, ?, ?)",
            (data.get('name'), data.get('email'), data.get('phone', ''), data.get('address', ''))
        )
        conn.commit()
        customer_id = cur.lastrowid
        conn.close()
        return self.get(customer_id)

    def update(self, customer_id, data):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE customers SET name = ?, email = ?, phone = ?, address = ? WHERE id = ?",
            (data.get('name'), data.get('email'), data.get('phone', ''), data.get('address', ''), customer_id)
        )
        conn.commit()
        conn.close()
        return self.get(customer_id)

    def delete(self, customer_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        conn.commit()
        deleted = cur.rowcount > 0
        conn.close()
        return deleted
