import pytest

from app.test.utils.functions import get_random_string, get_random_price


def test_create_pizza_size_service_returns_a_200_response(create_size):
    size = create_size.json
    pytest.assume(create_size.status.startswith('200'))
    pytest.assume(size['_id'])
    pytest.assume(size['name'])
    pytest.assume(size['price'])


def test_update_pizza_size_service_returns_a_200_response(client, create_size, size_url):
    current_size = create_size.json
    update_data = {**current_size, 'name': get_random_string(), 'price': get_random_price(1, 30)}
    response = client.put(size_url, json=update_data)
    pytest.assume(response.status.startswith('200'))
    updated_size = response.json
    for param, value in update_data.items():
        pytest.assume(updated_size[param] == value)


def test_get_pizza_size_by_id_service_returns_a_200_response(client, create_size, size_url):
    current_size = create_size.json
    response = client.get(f'{size_url}id/{current_size["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_size = response.json
    for param, value in current_size.items():
        pytest.assume(returned_size[param] == value)


def test_get_pizza_size_service_returns_a_200_response(client, create_sizes, size_url):
    response = client.get(size_url)
    pytest.assume(response.status.startswith('200'))
    returned_sizes = {size['_id']: size for size in response.json}
    for size in create_sizes:
        pytest.assume(size['_id'] in returned_sizes)
