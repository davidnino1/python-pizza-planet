from app.common.singleton import Singleton
from ..repositories.managers import SizeManager
from .base import BaseController


class SizeController(BaseController, metaclass=Singleton):
    manager = SizeManager
