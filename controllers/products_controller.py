from services.product_service import ProductService
from core.responses import ok, created, err


service = ProductService()


def list_products():
    return ok(service.list_all())


def create_product(data):
    try:
        created_item = service.create(data)
        return created(created_item)
    except Exception as e:
        return err(str(e), 500)


def get_product(product_id):
    item = service.get(product_id)
    if not item:
        return err('Not found', 404)
    return ok(item)


def update_product(product_id, data):
    updated = service.update(product_id, data)
    if not updated:
        return err('Not found', 404)
    return ok(updated)


def delete_product(product_id):
    deleted = service.delete(product_id)
    if not deleted:
        return err('Not found', 404)
    return ok({'deleted': product_id})
