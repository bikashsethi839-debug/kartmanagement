from fastapi import APIRouter, Request
from core.responses import ok, created, err
from services.product_service import ProductService
from services.review_service import ReviewService

product_router = APIRouter(prefix="/api/products")
service = ProductService()
review_service = ReviewService()

@product_router.get("")
def list_products():
    items = service.list_all()
    return ok(items)

@product_router.post("")
async def create_product(request: Request):
    data = await request.json() or {}
    created_item = service.create(data)
    return created(created_item)

@product_router.get("/{product_id}")
def get_product(product_id: int):
    item = service.get(product_id)
    if not item:
        return err('Not found', 404)
    return ok(item)

@product_router.put("/{product_id}")
async def update_product(product_id: int, request: Request):
    data = await request.json() or {}
    updated = service.update(product_id, data)
    if not updated:
        return err('Not found', 404)
    return ok(updated)

@product_router.delete("/{product_id}")
def delete_product(product_id: int):
    deleted = service.delete(product_id)
    if not deleted:
        return err('Not found', 404)
    return ok({'deleted': product_id})

@product_router.post("/{product_id}/duplicate")
def duplicate_product(product_id: int):
    new_item = service.duplicate(product_id)
    if not new_item:
        return err('Not found', 404)
    return created(new_item)

@product_router.post("/bulk-delete")
async def bulk_delete_products(request: Request):
    payload = await request.json() or {}
    ids = payload.get('ids', [])
    if not isinstance(ids, list) or not ids:
        return err('Provide ids list', 400)
    deleted = service.bulk_delete(ids)
    return ok({'deleted_count': deleted})

# Reviews endpoints
@product_router.get("/{product_id}/reviews")
def list_reviews(product_id: int):
    reviews = review_service.list_for_product(product_id)
    return ok(reviews)

@product_router.post("/{product_id}/reviews")
async def create_review(product_id: int, request: Request):
    data = await request.json() or {}
    created_review = review_service.create(product_id, data)
    return created(created_review)

@product_router.delete("/{product_id}/reviews/{review_id}")
def delete_review(product_id: int, review_id: int):
    deleted = review_service.delete(review_id)
    if not deleted:
        return err('Not found', 404)
    return ok({'deleted': review_id})
