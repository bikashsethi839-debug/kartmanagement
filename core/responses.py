def ok(data=None):
    return {"status": "ok", "data": data}


def created(data=None):
    return {"status": "created", "data": data}


def err(message, code=400):
    return {"status": "error", "message": message}
