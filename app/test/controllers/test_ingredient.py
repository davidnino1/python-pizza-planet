import pytest
from app.controllers import IngredientController


def test_create_ingredient_returns_created_service_when_created_correctly(app, ingredient: dict):
    created_ingredient, error = IngredientController.create(ingredient)
    pytest.assume(error is None)
    for param, value in ingredient.items():
        pytest.assume(param in created_ingredient)
        pytest.assume(value == created_ingredient[param])
        pytest.assume(created_ingredient['_id'])


def test_update_ingredient_returns_updated_service_when_exists_in_database(app, ingredient: dict):
    created_ingredient, _ = IngredientController.create(ingredient)
    updated_fields = {
        'name': 'updated',
        'price': 10
    }
    updated_ingredient, error = IngredientController.update({
        '_id': created_ingredient['_id'],
        **updated_fields
    })
    pytest.assume(error is None)
    ingredient_from_database, error = IngredientController.get_by_id(created_ingredient['_id'])
    pytest.assume(error is None)
    for param, value in updated_fields.items():
        pytest.assume(updated_ingredient[param] == value)
        pytest.assume(ingredient_from_database[param] == value)


def test_get_ingredient_by_id_returns_ingredient_when_exists_in_database(app, ingredient: dict):
    created_ingredient, _ = IngredientController.create(ingredient)
    ingredient_from_db, error = IngredientController.get_by_id(created_ingredient['_id'])
    pytest.assume(error is None)
    for param, value in created_ingredient.items():
        pytest.assume(ingredient_from_db[param] == value)


def test_get_all_ingredients_when_one_or_more_exist_in_database(app, ingredients: list):
    created_ingredients = []
    for ingredient in ingredients:
        created_ingredient, _ = IngredientController.create(ingredient)
        created_ingredients.append(created_ingredient)

    ingredients_from_db, error = IngredientController.get_all()
    searchable_ingredients = {db_ingredient['_id']: db_ingredient for db_ingredient in ingredients_from_db}
    pytest.assume(error is None)
    for created_ingredient in created_ingredients:
        current_id = created_ingredient['_id']
        assert current_id in searchable_ingredients
        for param, value in created_ingredient.items():
            pytest.assume(searchable_ingredients[current_id][param] == value)
