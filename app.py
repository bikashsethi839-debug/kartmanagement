from flask import Flask, send_from_directory
from router import register_routes
from database.complaintstable import init_db
import argparse
import sys

app = Flask(__name__, static_folder="frontend/assets", template_folder="frontend/pages")

# Register routes (API + page routes)
register_routes(app)

@app.route('/')
def index():
    return send_from_directory('frontend/pages', 'catalog.html')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--init-db', action='store_true', help='Initialize the SQLite database and seed data')
    args = parser.parse_args()

    if args.init_db:
        init_db()
        print('DB initialized')
        sys.exit(0)

    # Ensure DB exists (safe to call multiple times)
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
