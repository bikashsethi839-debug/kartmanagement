from .connection import get_connection
from .queries import CREATE_PRODUCTS_TABLE, CREATE_CART_TABLE, SEED_PRODUCTS


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.executescript(CREATE_PRODUCTS_TABLE)
    cur.executescript(CREATE_CART_TABLE)

    # Seed
    cur.executemany(
        "INSERT OR IGNORE INTO products (name, sku, price, stock, description) VALUES (?, ?, ?, ?, ?)",
        SEED_PRODUCTS
    )
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    print('DB initialized')
