import pytest

from app.test.utils.functions import get_random_string, get_random_price


def test_create_beverage_service_returns_a_200_response(create_beverage):
    beverage = create_beverage.json
    pytest.assume(create_beverage.status.startswith('200'))
    pytest.assume(beverage['_id'])
    pytest.assume(beverage['name'])
    pytest.assume(beverage['price'])


def test_update_beverage_service_returns_a_200_response(client, create_beverage, beverage_url):
    current_beverage = create_beverage.json
    update_data = {**current_beverage, 'name': get_random_string(), 'price': get_random_price(1, 5)}
    response = client.put(beverage_url, json=update_data)
    pytest.assume(response.status.startswith('200'))
    updated_beverage = response.json
    for param, value in update_data.items():
        pytest.assume(updated_beverage[param] == value)


def test_get_beverage_by_id_service_returns_a_200_response(client, create_beverage, beverage_url):
    current_beverage = create_beverage.json
    response = client.get(f'{beverage_url}id/{current_beverage["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_beverage = response.json
    for param, value in current_beverage.items():
        pytest.assume(returned_beverage[param] == value)


def test_get_beverages_service_returns_a_200_response(client, create_beverages, beverage_url):
    response = client.get(beverage_url)
    pytest.assume(response.status.startswith('200'))
    returned_beverages = {beverage['_id']: beverage for beverage in response.json}
    for beverage in create_beverages:
        pytest.assume(beverage['_id'] in returned_beverages)
