from typing import Tuple
from sqlalchemy.exc import SQLAlchemyError

from app.common.singleton import Singleton

from ..repositories.managers import IndexManager


class IndexController(metaclass=Singleton):

    @staticmethod
    def test_connection() -> Tuple[bool, str]:
        try:
            IndexManager.test_connection()
            return True, ''
        except (SQLAlchemyError, RuntimeError) as ex:
            return False, str(ex)
