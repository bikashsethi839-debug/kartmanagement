from services.wishlist_service import WishlistService
from core.responses import ok, created, err


service = WishlistService()


def list_wishlist():
    return ok(service.list_all())


def add_to_wishlist(data):
    try:
        created_item = service.add(data)
        return created(created_item)
    except Exception as e:
        return err(str(e), 500)


def remove_from_wishlist(item_id):
    deleted = service.delete(item_id)
    if not deleted:
        return err('Not found', 404)
    return ok({'deleted': item_id})
