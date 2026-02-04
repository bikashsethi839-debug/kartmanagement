from fastapi import APIRouter, Request
from core.responses import ok, created, err
from services.cart_service import CartService
from services.wishlist_service import WishlistService

cart_router = APIRouter(prefix="/api/cart")
cart_service = CartService()
wishlist_service = WishlistService()

@cart_router.get("")
def list_cart():
    items = cart_service.list_all()
    return ok(items)

@cart_router.post("")
async def add_to_cart(request: Request):
    data = await request.json() or {}
    created_item = cart_service.add(data)
    return created(created_item)

@cart_router.put("/{item_id}")
async def update_item(item_id: int, request: Request):
    data = await request.json() or {}
    updated = cart_service.update(item_id, data)
    if not updated:
        return err('Not found', 404)
    return ok(updated)

@cart_router.delete("/{item_id}")
def delete_item(item_id: int):
    deleted = cart_service.delete(item_id)
    if not deleted:
        return err('Not found', 404)
    return ok({'deleted': item_id})

# Wishlist endpoints
@cart_router.get("/wishlist")
def list_wishlist():
    items = wishlist_service.list_all()
    return ok(items)

@cart_router.post("/wishlist")
async def add_wishlist(request: Request):
    data = await request.json() or {}
    created_item = wishlist_service.add(data)
    return created(created_item)

@cart_router.delete("/wishlist/{item_id}")
def delete_wishlist(item_id: int):
    deleted = wishlist_service.delete(item_id)
    if not deleted:
        return err('Not found', 404)
    return ok({'deleted': item_id})
