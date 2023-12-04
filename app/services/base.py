from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request
from app.services.responses import OK, BAD_REQUEST, NOT_FOUND


from ..controllers.base import BaseController

from functools import wraps
from flask import jsonify


def base_service(controller):
    @wraps(controller)
    def wrapper(*args, **kwargs):
        result, error = controller(*args, **kwargs)
        response = result if not error else {'error': error}
        status_code = OK if not error else BAD_REQUEST
        return jsonify(response), status_code
    return wrapper
