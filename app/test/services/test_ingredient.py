import pytest

from app.test.utils.functions import get_random_string, get_random_price


def test_create_ingredient_service_returns_a_200_response(create_ingredient):
    ingredient = create_ingredient.json
    pytest.assume(create_ingredient.status.startswith('200'))
    pytest.assume(ingredient['_id'])
    pytest.assume(ingredient['name'])
    pytest.assume(ingredient['price'])


def test_update_ingredient_service_returns_a_200_response(client, create_ingredient, ingredient_url):
    current_ingredient = create_ingredient.json
    update_data = {**current_ingredient, 'name': get_random_string(), 'price': get_random_price(1, 5)}
    response = client.put(ingredient_url, json=update_data)
    pytest.assume(response.status.startswith('200'))
    updated_ingredient = response.json
    for param, value in update_data.items():
        pytest.assume(updated_ingredient[param] == value)


def test_get_ingredient_by_id_service_returns_a_200_response(client, create_ingredient, ingredient_url):
    current_ingredient = create_ingredient.json
    response = client.get(f'{ingredient_url}id/{current_ingredient["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_ingredient = response.json
    for param, value in current_ingredient.items():
        pytest.assume(returned_ingredient[param] == value)


def test_get_ingredients_service_returns_a_200_response(client, create_ingredients, ingredient_url):
    response = client.get(ingredient_url)
    pytest.assume(response.status.startswith('200'))
    returned_ingredients = {ingredient['_id']: ingredient for ingredient in response.json}
    for ingredient in create_ingredients:
        pytest.assume(ingredient['_id'] in returned_ingredients)
