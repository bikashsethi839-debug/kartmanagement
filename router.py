"""Router module - provides the HTTP request handler for the application."""

import sys
import os
import json
import urllib.parse
from http.server import BaseHTTPRequestHandler

from core.responses import ok, created, err
from controllers import products_controller
from controllers import cart_controller
from controllers import wishlist_controller


class KartRouter(BaseHTTPRequestHandler):
    """HTTP request handler for all API and static routes."""

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
        try:
            # Products API
            if path == '/api/products' and self.command == 'GET':
                response = products_controller.list_products()
                self.send_json_response(response)
                return
            if path == '/api/products' and self.command == 'POST':
                data = self.get_request_data()
                response = products_controller.create_product(data)
                self.send_json_response(response, 201 if response.get('status') == 'created' else 400)
                return
            if path.startswith('/api/products/'):
                try:
                    product_id = int(path.split('/')[-1])
                except Exception:
                    self.send_json_response(err('Invalid id', 400), 400)
                    return

                if self.command == 'GET':
                    response = products_controller.get_product(product_id)
                    self.send_json_response(response, 200 if response.get('status') == 'ok' else 404)
                    return
                if self.command == 'PUT':
                    data = self.get_request_data()
                    response = products_controller.update_product(product_id, data)
                    self.send_json_response(response, 200 if response.get('status') == 'ok' else 404)
                    return
                if self.command == 'DELETE':
                    response = products_controller.delete_product(product_id)
                    self.send_json_response(response, 200 if response.get('status') == 'ok' else 404)
                    return

            # Cart API
            if path == '/api/cart' and self.command == 'GET':
                response = cart_controller.list_cart()
                self.send_json_response(response)
                return
            if path == '/api/cart' and self.command == 'POST':
                data = self.get_request_data()
                response = cart_controller.add_to_cart(data)
                self.send_json_response(response, 201 if response.get('status') == 'created' else 400)
                return
            if path.startswith('/api/cart/') and not path.startswith('/api/cart/wishlist'):
                try:
                    item_id = int(path.split('/')[-1])
                except Exception:
                    self.send_json_response(err('Invalid id', 400), 400)
                    return

                if self.command == 'PUT':
                    data = self.get_request_data()
                    response = cart_controller.update_cart_item(item_id, data)
                    self.send_json_response(response, 200 if response.get('status') == 'ok' else 404)
                    return
                if self.command == 'DELETE':
                    response = cart_controller.remove_from_cart(item_id)
                    self.send_json_response(response, 200 if response.get('status') == 'ok' else 404)
                    return

            # Wishlist API
            if path == '/api/cart/wishlist' and self.command == 'GET':
                response = wishlist_controller.list_wishlist()
                self.send_json_response(response)
                return
            if path == '/api/cart/wishlist' and self.command == 'POST':
                data = self.get_request_data()
                response = wishlist_controller.add_to_wishlist(data)
                self.send_json_response(response, 201 if response.get('status') == 'created' else 400)
                return
            if path.startswith('/api/cart/wishlist/'):
                try:
                    item_id = int(path.split('/')[-1])
                except Exception:
                    self.send_json_response(err('Invalid id', 400), 400)
                    return

                if self.command == 'DELETE':
                    response = wishlist_controller.remove_from_wishlist(item_id)
                    self.send_json_response(response, 200 if response.get('status') == 'ok' else 404)
                    return

            # Fallback: not found
            self.send_json_response(err('Not found', 404), 404)
        except Exception as e:
            self.send_json_response(err(str(e), 500), 500)

