import uuid

import numpy as np
import pandas as pd
from tqdm.auto import tqdm
from faker import Faker

from generator.config import *


def generate_users() -> pd.DataFrame:
    fake = Faker()
    # Установка сидов для воспроизводимости результатов
    Faker.seed(67)
    np.random.seed(67)

    creation_dates = pd.date_range(start=REGISTRATION_START, end=REGISTRATION_END)
    users_data = []

    for _ in tqdm(range(NUM_USERS), desc='Generating users'):
        user_id = uuid.uuid4().hex
        user = {
            'user_id': user_id,
            'name': fake.name(),
            'email': f"{user_id[:4]}_{fake.email()}",
            'registration_date': np.random.choice(creation_dates),
            'city': fake.city(),
            'state': fake.state_abbr(),
        }
        users_data.append(user)

    users_df = pd.DataFrame(users_data)

    # Проверка уникальности email и user_id
    assert users_df['email'].is_unique, 'Email not unique'
    assert users_df['user_id'].is_unique, 'User id not unique'

    return users_df


def generate_products() -> pd.DataFrame:
    fake = Faker()
    # Установка сидов для воспроизводимости результатов
    Faker.seed(67)
    np.random.seed(67)

    products_data = []

    for _ in tqdm(range(NUM_PRODUCTS), desc='Generating products'):

        category = np.random.choice(CATEGORIES)
        sub_category = np.random.choice(SUBCATEGORIES[category])

        price = np.random.normal(PRICE_MEAN, PRICE_STD)
        price = max(0.01, price)

        product = {
            'product_id': uuid.uuid4().hex,
            'category': category,
            'subcategory': sub_category,
            'product_name': f"{sub_category} {fake.bothify(text='Model ??-###')}",
            'base_price': round(price, 2)
        }

        products_data.append(product)

    products_df = pd.DataFrame(products_data)

    assert products_df['product_id'].is_unique, 'Product id not unique'
    assert (products_df['base_price'] > 0).all(), 'Found negative or zero price'

    return products_df
