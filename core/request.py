from flask import request


def json_body():
    return request.get_json(silent=True) or {}
