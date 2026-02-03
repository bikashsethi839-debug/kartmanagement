from flask import jsonify


def ok(data=None):
    payload = {"status": "ok", "data": data}
    return jsonify(payload), 200


def created(data=None):
    payload = {"status": "created", "data": data}
    return jsonify(payload), 201


def err(message, code=400):
    return jsonify({"status": "error", "message": message}), code
