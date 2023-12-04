
import pytest
from ..fixtures.report import *


def test_get_report_service_returns_a_200_response(client, report_url):
    response = client.get(report_url)
    pytest.assume(response.status.startswith('200'))
