from flask import Blueprint, jsonify, request, send_from_directory
from controllers.product_controller import product_bp
from controllers.cart_controller import cart_bp

def register_routes(app):
    api_bp = Blueprint('api', __name__, url_prefix='/api')

    # Register API blueprints
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)

    # Static page fallback
    @app.route('/<path:page>')
    def pages(page):
        try:
            return send_from_directory('frontend/pages', page)
        except Exception:
            return send_from_directory('frontend/pages', '404.html'), 404
