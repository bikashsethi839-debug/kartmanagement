# Kart Management (Employee Management Demo)

Simple Python 3.8 + Flask + SQLite web app demonstrating multi-page CRUD for products and cart.

Quick start

1. Create a virtualenv and activate it (Python 3.8 recommended):

   python -m venv .venv
   source .venv/bin/activate

2. Install dependencies:

   pip install -r requirements.txt

3. Initialize the database (optional - the server will auto-initialize on start):

   python app.py --init-db

4. Run the app:

   python app.py

5. Open http://localhost:5000 in your browser and navigate pages (Catalog, Dashboard, Inventory, Product, Cart).

Testing

- Run unit/integration tests with pytest:

  PYTHONPATH=. .venv/bin/python -m pytest -q

Notes

- The app uses a small SQLite database at `instance/app.db` by default.
- For tests, a temporary DB is used to avoid polluting the dev DB.
