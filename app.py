"""Starts the API server and initializes the database."""

import sys
import os
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

from database.complaintstable import init_db
from services.product_service import ProductService
from services.cart_service import CartService
from services.review_service import ReviewService
from services.wishlist_service import WishlistService
from services.customer_service import CustomerService
from services.order_service import OrderService
from core.responses import ok, created, err

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    allow_reuse_address = True

class KartRouter(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        sys.stderr.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def do_PUT(self):
        self.handle_request()

    def do_DELETE(self):
        self.handle_request()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def handle_request(self):
        path = urllib.parse.urlparse(self.path).path
        
        if path.startswith('/assets/'):
            self.serve_static_file(path)
            return
        
        if path.startswith('/api/'):
            self.handle_api_request(path)
            return
        
        if path == '/':
            self.serve_file('frontend/pages/catalog.html')
        else:
            page_path = f'frontend/pages{path}'
            if os.path.exists(page_path) and os.path.isfile(page_path):
                self.serve_file(page_path)
            else:
                self.serve_file('frontend/pages/404.html', 404)

    def serve_static_file(self, path):
        file_path = 'frontend' + path
        if os.path.exists(file_path) and os.path.isfile(file_path):
            self.serve_file(file_path)
        else:
            self.send_error(404)

    def serve_file(self, file_path, status=200):
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            self.send_response(status)
            if file_path.endswith('.html'):
                self.send_header('Content-type', 'text/html; charset=utf-8')
            elif file_path.endswith('.css'):
                self.send_header('Content-type', 'text/css; charset=utf-8')
            elif file_path.endswith('.js'):
                self.send_header('Content-type', 'application/javascript; charset=utf-8')
            elif file_path.endswith('.json'):
                self.send_header('Content-type', 'application/json; charset=utf-8')
            elif file_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                ext = file_path.split('.')[-1]
                self.send_header('Content-type', f'image/{ext}')
            else:
                self.send_header('Content-type', 'application/octet-stream')
            self.send_header('Content-Length', str(len(content)))
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404)
        except Exception as e:
            print(f'Error serving {file_path}: {e}')
            self.send_error(500)

    def get_request_data(self):
        if 'Content-Length' in self.headers:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                return json.loads(post_data.decode('utf-8'))
            except:
                return {}
        return {}

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def handle_api_request(self, path):
        product_service = ProductService()
        cart_service = CartService()
        review_service = ReviewService()
        wishlist_service = WishlistService()
        customer_service = CustomerService()
        order_service = OrderService()
        
        try:
            if path == '/api/products' and self.command == 'GET':
                items = product_service.list_all()
                self.send_json_response(ok(items))
            elif path == '/api/products' and self.command == 'POST':
                data = self.get_request_data()
                created_item = product_service.create(data)
                self.send_json_response(created(created_item), 201)
            elif path.startswith('/api/products/') and self.command == 'GET':
                product_id = int(path.split('/')[-1])
                item = product_service.get(product_id)
                if not item:
                    self.send_json_response(err('Not found', 404), 404)
                else:
                    self.send_json_response(ok(item))
            elif path.startswith('/api/products/') and self.command == 'PUT':
                product_id = int(path.split('/')[-1])
                data = self.get_request_data()
                updated = product_service.update(product_id, data)
                if not updated:
                    self.send_json_response(err('Not found', 404), 404)
                else:
                    self.send_json_response(ok(updated))
            elif path.startswith('/api/products/') and self.command == 'DELETE':
                product_id = int(path.split('/')[-1])
                deleted = product_service.delete(product_id)
                if not deleted:
                    self.send_json_response(err('Not found', 404), 404)
                else:
                    self.send_json_response(ok({'deleted': product_id}))
            elif path == '/api/cart' and self.command == 'GET':
                items = cart_service.list_all()
                self.send_json_response(ok(items))
            elif path == '/api/cart' and self.command == 'POST':
                data = self.get_request_data()
                created_item = cart_service.add(data)
                self.send_json_response(created(created_item), 201)
            elif path.startswith('/api/cart/') and self.command == 'PUT':
                item_id = int(path.split('/')[-1])
                data = self.get_request_data()
                updated = cart_service.update(item_id, data)
                if not updated:
                    self.send_json_response(err('Not found', 404), 404)
                else:
                    self.send_json_response(ok(updated))
            elif path.startswith('/api/cart/') and self.command == 'DELETE':
                item_id = int(path.split('/')[-1])
                deleted = cart_service.delete(item_id)
                if not deleted:
                    self.send_json_response(err('Not found', 404), 404)
                else:
                    self.send_json_response(ok({'deleted': item_id}))
            elif path == '/api/cart/wishlist' and self.command == 'GET':
                items = wishlist_service.list_all()
                self.send_json_response(ok(items))
            elif path == '/api/cart/wishlist' and self.command == 'POST':
                data = self.get_request_data()
                created_item = wishlist_service.add(data)
                self.send_json_response(created(created_item), 201)
            elif path.startswith('/api/cart/wishlist/') and self.command == 'DELETE':
                item_id = int(path.split('/')[-1])
                deleted = wishlist_service.delete(item_id)
                if not deleted:
                    self.send_json_response(err('Not found', 404), 404)
                else:
                    self.send_json_response(ok({'deleted': item_id}))
            
            # Customer API
            elif path == '/api/customers' and self.command == 'GET':
                items = customer_service.list_all()
                self.send_json_response(ok(items))
            elif path == '/api/customers' and self.command == 'POST':
                data = self.get_request_data()
                created_item = customer_service.create(data)
                self.send_json_response(created(created_item), 201)
            elif path.startswith('/api/customers/') and path.endswith('/orders') and self.command == 'GET':
                customer_id = int(path.split('/')[-2])
                orders = order_service.get_customer_orders(customer_id)
                self.send_json_response(ok(orders))
            elif path.startswith('/api/customers/') and self.command == 'GET':
                customer_id = int(path.split('/')[-1])
                item = customer_service.get(customer_id)
                if not item:
                    self.send_json_response(err('Not found', 404), 404)
                else:
                    self.send_json_response(ok(item))
            elif path.startswith('/api/customers/') and self.command == 'PUT':
                customer_id = int(path.split('/')[-1])
                data = self.get_request_data()
                updated = customer_service.update(customer_id, data)
                if not updated:
                    self.send_json_response(err('Not found', 404), 404)
                else:
                    self.send_json_response(ok(updated))
            elif path.startswith('/api/customers/') and self.command == 'DELETE':
                customer_id = int(path.split('/')[-1])
                deleted = customer_service.delete(customer_id)
                if not deleted:
                    self.send_json_response(err('Not found', 404), 404)
                else:
                    self.send_json_response(ok({'deleted': customer_id}))
            
            # Order API
            elif path == '/api/orders' and self.command == 'GET':
                items = order_service.list_all()
                self.send_json_response(ok(items))
            elif path == '/api/orders' and self.command == 'POST':
                data = self.get_request_data()
                created_item = order_service.create(data)
                self.send_json_response(created(created_item), 201)
            elif path.startswith('/api/orders/') and path.endswith('/items') and self.command == 'GET':
                order_id = int(path.split('/')[-2])
                items = order_service.get_order_items(order_id)
                self.send_json_response(ok(items))
            elif path.startswith('/api/orders/') and self.command == 'GET':
                order_id = int(path.split('/')[-1])
                item = order_service.get(order_id)
                if not item:
                    self.send_json_response(err('Not found', 404), 404)
                else:
                    self.send_json_response(ok(item))
            elif path.startswith('/api/orders/') and self.command == 'DELETE':
                order_id = int(path.split('/')[-1])
                deleted = order_service.delete(order_id)
                if not deleted:
                    self.send_json_response(err('Not found', 404), 404)
                else:
                    self.send_json_response(ok({'deleted': order_id}))
            else:
                self.send_json_response(err('Not found', 404), 404)
        except Exception as e:
            self.send_json_response(err(str(e), 500), 500)


def run_server():
    init_db()
    server = ThreadedHTTPServer(("", 8000), KartRouter)
    print("🚀 Server running at http://localhost:8000")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
