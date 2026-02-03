import os
from .connection import get_connection, DB_PATH
from .queries import CREATE_PRODUCTS_TABLE, CREATE_CART_TABLE, CREATE_REVIEWS_TABLE, CREATE_WISHLIST_TABLE, SEED_PRODUCTS, SEED_REVIEWS


def init_db():
    # In test mode (PYTEST_DB), ensure DB starts clean to avoid unique-key collisions across tests
    if os.getenv('PYTEST_DB'):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

    conn = get_connection()
    cur = conn.cursor()
    cur.executescript(CREATE_PRODUCTS_TABLE)
    cur.executescript(CREATE_CART_TABLE)
    cur.executescript(CREATE_REVIEWS_TABLE)
    cur.executescript(CREATE_WISHLIST_TABLE)

    # Seed
    cur.executemany(
        "INSERT OR IGNORE INTO products (name, sku, price, stock, description) VALUES (?, ?, ?, ?, ?)",
        SEED_PRODUCTS
    )

    # Seed reviews (only if product with id exists)
    try:
        cur.executemany(
            "INSERT OR IGNORE INTO reviews (product_id, author, rating, comment) VALUES (?, ?, ?, ?)",
            SEED_REVIEWS
        )
    except Exception:
        # ignore if id not present yet
        pass

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    print('DB initialized')
