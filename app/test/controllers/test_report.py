import pytest
from app.controllers import ReportController


def test_get_report(app):
    report_controller = ReportController()
    pytest.assume(report_controller.get_report())

def test_get_top_month(app):
    report_controller = ReportController()
    pytest.assume(report_controller.get_top_month() is not None)

def test_get_top_ingredient(app):
    report_controller = ReportController()
    pytest.assume(report_controller.get_top_ingredient() is not None)

def test_get_top_customers(app):
    report_controller = ReportController()
    pytest.assume(report_controller.get_top_customers() is not None)
