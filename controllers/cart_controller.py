from flask import Blueprint
from core.responses import ok, created, err
from core.request import json_body
from services.cart_service import CartService

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')
service = CartService()

@cart_bp.route('', methods=['GET'])
def list_cart():
    items = service.list_all()
    return ok(items)

@cart_bp.route('', methods=['POST'])
def add_to_cart():
    data = json_body()
    created_item = service.add(data)
    return created(created_item)

@cart_bp.route('/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = json_body()
    updated = service.update(item_id, data)
    if not updated:
        return err('Not found', 404)
    return ok(updated)

@cart_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    deleted = service.delete(item_id)
    if not deleted:
        return err('Not found', 404)
    return ok({'deleted': item_id})
