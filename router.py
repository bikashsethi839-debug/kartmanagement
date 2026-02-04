from fastapi import FastAPI
from fastapi.responses import FileResponse
from controllers.product_controller import product_router
from controllers.cart_controller import cart_router
import os


def register_routes(app: FastAPI):
    app.include_router(product_router)
    app.include_router(cart_router)

    @app.get("/{page:path}")
    def pages(page: str):
        path = os.path.join("frontend/pages", page)
        if os.path.exists(path):
            return FileResponse(path)
        return FileResponse("frontend/pages/404.html", status_code=404)
