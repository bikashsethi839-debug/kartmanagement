from fastapi.responses import JSONResponse


def ok(data=None):
    payload = {"status": "ok", "data": data}
    return JSONResponse(content=payload, status_code=200)


def created(data=None):
    payload = {"status": "created", "data": data}
    return JSONResponse(content=payload, status_code=201)


def err(message, code=400):
    return JSONResponse(content={"status": "error", "message": message}, status_code=code)
