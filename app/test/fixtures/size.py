import pytest

from ..utils.functions import get_random_price, get_random_string


def size_mock() -> dict:
    return {
        'name': get_random_string(),
        'price': get_random_price(10, 20)
    }


@pytest.fixture
def size_url():
    return '/size/'


@pytest.fixture
def size():
    return size_mock()


@pytest.fixture
def sizes():
    return [size_mock() for _ in range(5)]


@pytest.fixture
def create_size(client, size_url) -> dict:
    response = client.post(size_url, json=size_mock())
    return response


@pytest.fixture
def create_sizes(client, size_url) -> list:
    sizes = []
    for _ in range(10):
        new_size = client.post(size_url, json=size_mock())
        sizes.append(new_size.json)
    return sizes
