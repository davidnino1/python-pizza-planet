from faker import Faker
from app.seed.constants import NUMBER_CLIENTS, NUMBER_ORDERS, NUMBER_BEVERAGES, NUMBER_INGREDIENTS, NUMBER_SIZES
from app.seed.data import fake_beverages, fake_ingredients, fake_sizes
from app.seed.utils.seed_utils import (
    generate_random_beverages,
    generate_random_client,
    generate_random_ingredients,
    generate_random_sizes,
    get_random_sample,
    get_random_item
)

fake = Faker()

from app.repositories.managers import SizeManager, IngredientManager, BeverageManager, OrderManager


def insert_sizes(sizes: list):
    for size in sizes:
        SizeManager.create(size)


def insert_ingredients(ingredients: list):
    for ingredient in ingredients:
        IngredientManager.create(ingredient)


def insert_beverages(beverages: list):
    for beverage in beverages:
        BeverageManager.create(beverage)


def insert_orders(sizes: list, ingredients: list, beverages: list, clients: list):
    for _ in range(NUMBER_ORDERS):
        client_order = get_random_item(clients)
        size_order = get_random_item(sizes)
        ingredients_order = get_random_sample(ingredients, NUMBER_INGREDIENTS)
        beverages_order = get_random_sample(beverages, NUMBER_BEVERAGES)

        total_price = round(
            sum(ingredient.get("price") for ingredient in ingredients_order) + \
            sum(beverage.get("price") for beverage in beverages_order) + \
            size_order.get("price"), 2
        )

        order = client_order | {
            "date": fake.date_time_between(start_date="-1y", end_date="now", tzinfo=None),
            "size_id": size_order.get("_id"),
            "total_price": total_price
        }

        ingredients_ids = IngredientManager.get_by_id_list(
            [ingredient.get('_id') for ingredient in ingredients_order]
        )
        beverages_ids = BeverageManager.get_by_id_list(
            [beverage.get('_id') for beverage in beverages_order]
        )

        OrderManager.create(
            order_data=order,
            ingredients=ingredients_ids,
            beverages=beverages_ids,
        )


def seed():
    insert_sizes(sizes=generate_random_sizes(fake_sizes))
    insert_ingredients(ingredients=generate_random_ingredients(fake_ingredients))
    insert_beverages(beverages=generate_random_beverages(fake_beverages))

    insert_orders(
        sizes=SizeManager.get_all(),
        ingredients=IngredientManager.get_all(),
        beverages=BeverageManager.get_all(),
        clients=[generate_random_client() for _ in range(NUMBER_CLIENTS)]
    )
    print("DB seeded succesfully")
