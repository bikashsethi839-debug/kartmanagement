from flask import Blueprint, request
from core.request import json_body
from core.responses import ok, created, err
from services.review_service import ReviewService

review_bp = Blueprint('reviews', __name__, url_prefix='/api/reviews')
service = ReviewService()

@review_bp.route('/product/<int:product_id>', methods=['GET'])
def list_reviews(product_id):
    items = service.list_for_product(product_id)
    return ok(items)

@review_bp.route('/product/<int:product_id>', methods=['POST'])
def create_review(product_id):
    data = json_body()
    item = service.create(product_id, data)
    return created(item)
