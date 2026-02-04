from fastapi import Request


async def json_body(request: Request):
    try:
        return await request.json()
    except Exception:
        return {}
