async def json_body(request):
    """Compatibility shim: return an empty dict for non-JSON or unsupported request types.

    The project no longer depends on FastAPI; keep this async helper to avoid import
    errors where `json_body` may be referenced. It returns an empty dict by default.
    """
    try:
        # If `request` has an async `.json()` method (some test helpers), use it.
        if hasattr(request, 'json'):
            maybe = request.json()
            if hasattr(maybe, '__await__'):
                return await maybe
            return maybe
    except Exception:
        pass
    return {}
