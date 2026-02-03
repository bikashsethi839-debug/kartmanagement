from flask import Blueprint
from core.responses import ok, created, err
from core.request import json_body
from services.cart_service import CartService
from services.wishlist_service import WishlistService

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')
cart_service = CartService()
wishlist_service = WishlistService()

@cart_bp.route('', methods=['GET'])
def list_cart():
    items = cart_service.list_all()
    return ok(items)

@cart_bp.route('', methods=['POST'])
def add_to_cart():
    data = json_body()
    created_item = cart_service.add(data)
    return created(created_item)

@cart_bp.route('/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = json_body()
    updated = cart_service.update(item_id, data)
    if not updated:
        return err('Not found', 404)
    return ok(updated)

@cart_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    deleted = cart_service.delete(item_id)
    if not deleted:
        return err('Not found', 404)
    return ok({'deleted': item_id})

# Wishlist endpoints
@cart_bp.route('/wishlist', methods=['GET'])
def list_wishlist():
    items = wishlist_service.list_all()
    return ok(items)

@cart_bp.route('/wishlist', methods=['POST'])
def add_wishlist():
    data = json_body()
    created_item = wishlist_service.add(data)
    return created(created_item)

@cart_bp.route('/wishlist/<int:item_id>', methods=['DELETE'])
def delete_wishlist(item_id):
    deleted = wishlist_service.delete(item_id)
    if not deleted:
        return err('Not found', 404)
    return ok({'deleted': item_id})
