from flask import Flask, send_from_directory
from router import register_routes

app = Flask(__name__, static_folder="frontend/assets", template_folder="frontend/pages")

# Register routes (API + page routes)
register_routes(app)

@app.route('/')
def index():
    return send_from_directory('frontend/pages', 'catalog.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
