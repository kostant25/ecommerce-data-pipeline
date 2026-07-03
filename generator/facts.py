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

def generate_orders(carts_df) -> pd.DataFrame:
    np.random.seed(67)

    orders_data = []

    for _, cart in tqdm(carts_df.iterrows(), total=len(carts_df), desc='Generating orders'):

        if np.random.random() < ORDER_PROBABILITY:

            if np.random.random() < PAYMENT_PROBABILITY:
                status = 'delivered'
            else:
                status = 'cancelled'

            duration = (cart['end_time'] - cart['created_time']).total_seconds()
            max_offset = max(0, int(duration))
            offset = np.random.randint(0, max_offset + 1)  # 0 до max_offset включительно
            order_time = cart['created_time'] + pd.Timedelta(seconds=int(offset))

            orders_data.append({
                'order_id': uuid.uuid4().hex,
                'cart_id': cart['cart_id'],
                'user_id': cart['user_id'],
                'order_time': order_time,
                'status': status
            })

    orders_df = pd.DataFrame(orders_data)
    merged = orders_df.merge(carts_df[['cart_id', 'created_time', 'end_time']], on='cart_id')

    assert orders_df['order_id'].is_unique, 'Order is not unique'
    assert orders_df['cart_id'].is_unique, 'Card is not unique'
    assert merged['order_time'].between(merged['created_time'],
                                          merged['end_time']).all(), 'Order time outside session'

    return orders_df

def generate_payments(orders_df, cart_items_df, products_df) -> pd.DataFrame:
    np.random.seed(67)

    cart_prices = cart_items_df.merge(products_df[['product_id', 'base_price']], on='product_id')
    cart_prices['amount'] = cart_prices['quantity'] * cart_prices['base_price']

    carts = cart_prices.groupby('cart_id')['amount'].sum().reset_index()

    payment_orders = orders_df[orders_df['status'] == 'delivered'].merge(carts[['cart_id', 'amount']], on='cart_id')

    payments_data = []

    for _, payment in tqdm(payment_orders.iterrows(), total=len(payment_orders), desc='Generating payments'):

        method = np.random.choice(PAYMENT_METHODS)

        offset = np.random.randint(1, 3600)
        payment_time = payment['order_time'] + pd.Timedelta(seconds=int(offset))

        payments_data.append({
            'payment_id': uuid.uuid4().hex,
            'order_id': payment['order_id'],
            'amount': payment['amount'],
            'payment_time': payment_time,
            'method': method
        })

    payments_df = pd.DataFrame(payments_data)

    assert payments_df['payment_id'].is_unique, 'Payment id not unique'
    assert payments_df['order_id'].is_unique, 'Order id not unique'
    assert (payments_df['amount'] > 0).all(), 'Amount greater than 0'

    return payments_df