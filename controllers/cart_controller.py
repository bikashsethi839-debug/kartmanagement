from services.cart_service import CartService
from core.responses import ok, created, err


service = CartService()


def list_cart():
    return ok(service.list_all())


def add_to_cart(data):
    try:
        created_item = service.add(data)
        return created(created_item)
    except Exception as e:
        return err(str(e), 500)


def update_cart_item(item_id, data):
    updated = service.update(item_id, data)
    if not updated:
        return err('Not found', 404)
    return ok(updated)


def remove_from_cart(item_id):
    deleted = service.delete(item_id)
    if not deleted:
        return err('Not found', 404)
    return ok({'deleted': item_id})
