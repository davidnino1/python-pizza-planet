from app.common.singleton import Singleton
from ..repositories.managers import BeverageManager
from .base import BaseController


class BeverageController(BaseController, metaclass=Singleton):
    manager = BeverageManager
