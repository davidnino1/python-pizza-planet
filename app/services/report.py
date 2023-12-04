from app.common.http_methods import GET
from flask import Blueprint, jsonify
from app.services.responses import OK, BAD_REQUEST, NOT_FOUND

from ..controllers.report import ReportController

report = Blueprint('report', __name__)


@report.route('/', methods=GET)
def get_report():
    report_data, error = ReportController.get_report()
    response = report_data if not error else {'error': error}
    status_code = OK if report_data else NOT_FOUND if not error else BAD_REQUEST
    return jsonify(response), status_code
