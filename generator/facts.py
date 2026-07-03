import uuid

import pandas as pd
import numpy as np
from tqdm.auto import tqdm

from generator.config import *


def generate_sessions(users_df) -> pd.DataFrame:
    np.random.seed(67)

    event_start = pd.Timestamp(EVENT_START)
    event_end = pd.Timestamp(EVENT_END)

    sessions_data = []

    for _, user in tqdm(users_df.iterrows(), total=len(users_df), desc='Generating sessions'):
        curr_time = max(user['registration_date'], event_start)

        count_sessions = int(np.random.randint(low=1, high=5))

        for _ in range(count_sessions):
            gap = pd.Timedelta(seconds=int(np.random.randint(60, 86400)))
            start_time = curr_time + gap

            if start_time > event_end:
                break

            duration = pd.Timedelta(seconds=int(np.random.randint(low=10, high=1800)))
            end_time = start_time + duration

            curr_time = end_time

            sessions_data.append({
                'session_id': uuid.uuid4().hex,
                'user_id': user['user_id'],
                'start_time': start_time,
                'end_time': end_time,
                'device_type': np.random.choice(DEVICE_TYPES),
                'utm_source': np.random.choice(UTM_SOURCES),
            })

    sessions_df = pd.DataFrame(sessions_data)

    assert sessions_df['session_id'].is_unique, 'Session id not unique'

    return sessions_df

def generate_carts(sessions_df) -> pd.DataFrame:
    np.random.seed(67)

    carts_data = []

    for _, session in tqdm(sessions_df.iterrows(), total=len(sessions_df), desc='Generating carts'):

        if np.random.random() < CART_CREATION_PROBABILITY:

            duration = (session['end_time'] - session['start_time']).total_seconds()
            offset = np.random.randint(1, int(duration))
            created_time = session['start_time'] + pd.Timedelta(seconds=int(offset))

            carts_data.append({
                'cart_id': uuid.uuid4().hex,
                'user_id': session['user_id'],
                'session_id': session['session_id'],
                'created_time': created_time,
            })

    carts_df = pd.DataFrame(carts_data)
    merged = carts_df.merge(sessions_df[['session_id', 'start_time', 'end_time']], on='session_id')

    assert carts_df['cart_id'].is_unique, 'Cart id not unique'
    assert merged['created_time'].between(merged['start_time'], merged['end_time']).all(), 'Created time outside session'

    return carts_df

def generate_cart_items(carts_df, products_df) -> pd.DataFrame:
    np.random.seed(67)

    cart_items_data = []

    for _, cart in tqdm(carts_df.iterrows(), total=len(carts_df), desc='Generating cart items'):
        count_items = int(np.random.randint(low=CART_ITEM_MIN, high=CART_ITEM_MAX + 1))

        products = products_df.sample(count_items, replace=False)

        cart_item_id = 1

        for _, product in products.iterrows():

            if cart_item_id == 1:
                added_time = cart['created_time']
            else:
                duration = (cart['end_time'] - cart['created_time']).total_seconds()
                offset = np.random.randint(1, max(2, int(duration)))
                added_time = cart['created_time'] + pd.Timedelta(seconds=int(offset))

            cart_items_data.append({
                'cart_id': cart['cart_id'],
                'cart_item_id': cart_item_id,
                'product_id': product['product_id'],
                'quantity': int(np.random.randint(low=1, high=5)),
                'added_time': added_time
            })

            cart_item_id += 1

    cart_items_df = pd.DataFrame(cart_items_data)

    assert not cart_items_df.duplicated(subset=['cart_id', 'cart_item_id']).any()

    return cart_items_df