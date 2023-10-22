from ..repositories.managers import ReportManager
from .base import BaseController


class ReportController(BaseController):
    manager = ReportManager

    @classmethod
    def get_top_ingredient(cls):
        return cls.manager.get_top_ingredient()
    
    @classmethod
    def get_top_month(cls):
        return cls.manager.get_top_month()
    
    @classmethod
    def get_top_customers(cls):
        return cls.manager.get_top_customers()
    
    @classmethod
    def get_report(cls):
        report = {
            'top_customers': cls.get_top_customers(),
            'top_ingredient': cls.get_top_ingredient(),
            'top_month': cls.get_top_month()
        }
        return report, None