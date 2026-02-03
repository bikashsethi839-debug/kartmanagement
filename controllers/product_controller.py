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
