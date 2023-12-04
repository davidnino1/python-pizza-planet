from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request
from app.services.responses import OK, BAD_REQUEST, NOT_FOUND

from ..controllers.base import BaseController

class BaseService:
    def __init__(self, EntityController):
        self.controller = EntityController
    
    def create(self):
        beverage, error = self.controller.create(request.json)
        response = beverage if not error else {'error': error}
        status_code = OK if not error else BAD_REQUEST
        return jsonify(response), status_code


    def update(self):
        beverage, error = self.controller.update(request.json)
        response = beverage if not error else {'error': error}
        status_code = OK if not error else BAD_REQUEST
        return jsonify(response), status_code


    def get_by_id(self, _id: int):
        beverage, error = self.controller.get_by_id(_id)
        response = beverage if not error else {'error': error}
        status_code = OK if beverage else NOT_FOUND if not error else BAD_REQUEST
        return jsonify(response), status_code


    def get_all(self):
        beverages, error = self.controller.get_all()
        response = beverages if not error else {'error': error}
        status_code = OK if beverages else NOT_FOUND if not error else BAD_REQUEST
        return jsonify(response), status_code
