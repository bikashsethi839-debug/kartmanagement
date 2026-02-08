import argparse
import sys
import os

try:
    from fastapi import FastAPI
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse
    USE_FASTAPI = True
except ImportError:
    USE_FASTAPI = False

from database.complaintstable import init_db

if USE_FASTAPI:
    from router import register_routes
    
    app = FastAPI()
    # Mount static assets
    app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")
    
    # Register routes (API + page routes)
    register_routes(app)
    
    @app.get("/")
    def index():
        return FileResponse("frontend/pages/catalog.html")
else:
    # Custom HTTP server implementation
    import ssl
    import json
    import urllib.parse
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from socketserver import ThreadingMixIn
    
    from services.product_service import ProductService
    from services.cart_service import CartService
    from services.review_service import ReviewService
    from services.wishlist_service import WishlistService
    from core.responses import ok, created, err
    
    class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
        """Handle requests in a separate thread."""
        allow_reuse_address = True
    
    class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
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
                if os.path.exists(page_path):
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
                else:
                    self.send_json_response(err('Not found', 404), 404)
            except Exception as e:
                self.send_json_response(err(str(e), 500), 500)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--init-db', action='store_true', help='Initialize the SQLite database and seed data')
    parser.add_argument('--no-https', action='store_true', help='Disable HTTPS and run plain HTTP')
    args = parser.parse_args()

    if args.init_db:
        init_db()
        print('DB initialized')
        sys.exit(0)

    init_db()
    
    if USE_FASTAPI:
        import uvicorn
        cert_dir = os.path.join(os.getcwd(), 'certs')
        cert_key = os.path.join(cert_dir, 'dev.key')
        cert_crt = os.path.join(cert_dir, 'dev.crt')

        if not args.no_https and os.path.isfile(cert_key) and os.path.isfile(cert_crt):
            uvicorn.run('app:app', host='0.0.0.0', port=5000, reload=True,
                        ssl_keyfile=cert_key, ssl_certfile=cert_crt)
        else:
            uvicorn.run('app:app', host='0.0.0.0', port=5000, reload=True)
    else:
        cert_dir = os.path.join(os.getcwd(), 'certs')
        cert_key = os.path.join(cert_dir, 'dev.key')
        cert_crt = os.path.join(cert_dir, 'dev.crt')

        if not args.no_https:
            if not (os.path.isfile(cert_key) and os.path.isfile(cert_crt)):
                try:
                    os.makedirs(cert_dir, exist_ok=True)
                    import subprocess
                    subprocess.run([
                        'openssl', 'req', '-x509', '-nodes', '-days', '365', '-newkey', 'rsa:2048',
                        '-subj', '/CN=localhost', '-keyout', cert_key, '-out', cert_crt
                    ], check=True)
                    print(f'Generated self-signed certs in {cert_dir}')
                except Exception as e:
                    print('Failed to generate self-signed certs, falling back to HTTP:', e)
                    args.no_https = True

        try:
            server = ThreadedHTTPServer(('0.0.0.0', 5000), CustomHTTPRequestHandler)
        except OSError as e:
            if e.errno == 98:
                print('Port 5000 is already in use. Please stop any existing server or use a different port.')
                sys.exit(1)
            raise
        
        if not args.no_https:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(cert_crt, cert_key)
            server.socket = context.wrap_socket(server.socket, server_side=True)
            print('Starting HTTPS server on https://localhost:5000')
        else:
            print('Starting HTTP server on http://localhost:5000')
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print('\nShutting down server...')
            server.shutdown()


if __name__ == '__main__':
    main()
