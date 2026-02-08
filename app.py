"""Starts the API server and initializes the database."""

from http.server import HTTPServer
from router import KartRouter
from database.complaintstable import init_db


def run_server():
    init_db()
    server = HTTPServer(("", 5000), KartRouter)
    print("🚀 Server running at http://localhost:5000")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
