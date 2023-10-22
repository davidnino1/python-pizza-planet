from app.common.singleton import Singleton
from ..repositories.managers import IngredientManager
from .base import BaseController


class IngredientController(BaseController, metaclass=Singleton):
    manager = IngredientManager
