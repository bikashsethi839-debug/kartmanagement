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
        # Handle root path
        if not page or page == "":
            return FileResponse("frontend/pages/catalog.html")
        
        path = os.path.join("frontend/pages", page)
        
        # Check if it's a file and exists
        if os.path.isfile(path):
            return FileResponse(path)
        
        # Return 404 page
        return FileResponse("frontend/pages/404.html", status_code=404)
