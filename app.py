import argparse
import sys
import os
try:
    from fastapi import FastAPI
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse
except ImportError:
    print("Missing dependencies: FastAPI and/or Uvicorn are not installed in the current Python environment.")
    print("Fix options:\n  1) Activate the project venv and run: source .venv/bin/activate && pip install -r requirements.txt")
    print("  2) Run the script with the project venv python directly: .venv/bin/python app.py --init-db")
    sys.exit(1)

from router import register_routes
from database.complaintstable import init_db

app = FastAPI()
# Mount static assets
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")

# Register routes (API + page routes)
register_routes(app)

@app.get("/")
def index():
    return FileResponse("frontend/pages/catalog.html")


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
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)


if __name__ == '__main__':
    main()
