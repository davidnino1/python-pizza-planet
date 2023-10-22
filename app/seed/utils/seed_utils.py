from random import sample
from faker import Faker
import random as rand

from app.seed.constants import MIN_PRICE, MAX_PRICE, MIN_PRICE_SIZE, MAX_PRICE_SIZE

fake = Faker()


def generate_random_client():
    return {
        "client_address": fake.street_address(),
        "client_dni": str(fake.random_number(digits=10)),
        "client_name": fake.name(),
        "client_phone": fake.phone_number(),
    }


def generate_random_price(minimum: float, maximum: float):
    return fake.pyint(min_value=minimum, max_value=maximum)

def generate_random_sizes(sizes: list):
    return [
        {"name": size, "price": generate_random_price(MIN_PRICE_SIZE, MAX_PRICE_SIZE)}
        for size in sizes
    ]


def generate_random_ingredients(ingredients: list):
    return [
        {"name": ingredient, "price": generate_random_price(MIN_PRICE, MAX_PRICE)}
        for ingredient in ingredients
    ]


def generate_random_beverages(beverages: list):
    return [
        {"name": beverage, "price": generate_random_price(MIN_PRICE, MAX_PRICE)}
        for beverage in beverages
    ]


def get_random_sample(items: list, length: int):
    sample_size = rand.randint(1, length)
    return sample(items, sample_size)


def get_random_item(items: list):
    return rand.choice(items)
