from database.complaintstable import init_db
from database.connection import get_connection


def test_init_db_creates_tables(tmp_path, monkeypatch):
    # Use a temp DB path
    monkeypatch.setenv('PYTEST_DB', '1')
    init_db()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
    assert cur.fetchone() is not None
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cart'")
    assert cur.fetchone() is not None
    conn.close()
