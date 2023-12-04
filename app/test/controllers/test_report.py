import pytest
from app.controllers import ReportController


def test_get_report_returns_a_report_with_database_data(app):
    report_controller = ReportController()
    pytest.assume(report_controller.get_report())

def test_get_top_month_returns_the_month_with_most_revenue_with_database_data(app):
    report_controller = ReportController()
    pytest.assume(report_controller.get_top_month() is not None)

def test_get_top_ingredient_returns_the_top_ingredient_with_database_data(app):
    report_controller = ReportController()
    pytest.assume(report_controller.get_top_ingredient() is not None)

def test_get_top_customers_returns_top_customers_with_database_data(app):
    report_controller = ReportController()
    pytest.assume(report_controller.get_top_customers() is not None)
