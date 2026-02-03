from flask import Blueprint, request
from core.responses import ok, created, err
from core.request import json_body
from services.product_service import ProductService

product_bp = Blueprint('products', __name__, url_prefix='/api/products')
service = ProductService()

@product_bp.route('', methods=['GET'])
def list_products():
    items = service.list_all()
    return ok(items)

@product_bp.route('', methods=['POST'])
def create_product():
    data = json_body()
    created_item = service.create(data)
    return created(created_item)

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    item = service.get(product_id)
    if not item:
        return err('Not found', 404)
    return ok(item)

@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = json_body()
    updated = service.update(product_id, data)
    if not updated:
        return err('Not found', 404)
    return ok(updated)

@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    deleted = service.delete(product_id)
    if not deleted:
        return err('Not found', 404)
    return ok({'deleted': product_id})

@product_bp.route('/<int:product_id>/duplicate', methods=['POST'])
def duplicate_product(product_id):
    new_item = service.duplicate(product_id)
    if not new_item:
        return err('Not found', 404)
    return created(new_item)

@product_bp.route('/bulk-delete', methods=['POST'])
def bulk_delete_products():
    payload = request.get_json(silent=True) or {}
    ids = payload.get('ids', [])
    if not isinstance(ids, list) or not ids:
        return err('Provide ids list', 400)
    deleted = service.bulk_delete(ids)
    return ok({'deleted_count': deleted})

# Reviews endpoints
from services.review_service import ReviewService
review_service = ReviewService()

@product_bp.route('/<int:product_id>/reviews', methods=['GET'])
def list_reviews(product_id):
    reviews = review_service.list_for_product(product_id)
    return ok(reviews)

@product_bp.route('/<int:product_id>/reviews', methods=['POST'])
def create_review(product_id):
    data = json_body()
    created_review = review_service.create(product_id, data)
    return created(created_review)

@product_bp.route('/<int:product_id>/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(product_id, review_id):
    deleted = review_service.delete(review_id)
    if not deleted:
        return err('Not found', 404)
    return ok({'deleted': review_id})
