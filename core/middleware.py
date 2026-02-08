"""Middleware helpers (scaffold).

These helpers can be used by server handlers to apply cross-cutting concerns
like CORS and basic request logging.
"""

def add_cors_headers(send_header_fn):
    """Call `send_header_fn(key, value)` for required CORS headers."""
    send_header_fn('Access-Control-Allow-Origin', '*')
    send_header_fn('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    send_header_fn('Access-Control-Allow-Headers', 'Content-Type')


def log_request(addr, method, path):
    print(f"{addr} - {method} {path}")
