import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generator.config import *
from generator.dimensions import generate_users, generate_products
from generator.facts import generate_sessions, generate_carts, generate_cart_items, generate_orders, generate_payments


def main():
    # Generating data
    print("Generating fake data start")

    users = generate_users()
    products = generate_products()

    sessions = generate_sessions(users)
    carts = generate_carts(sessions)

    cart_with_session_time = carts.merge(sessions[['session_id', 'end_time']], on='session_id')

    cart_items = generate_cart_items(cart_with_session_time, products)
    orders = generate_orders(cart_with_session_time)
    payments = generate_payments(orders, cart_items, products)

    # Validating data
    # Связи пользователей
    assert sessions['user_id'].isin(users['user_id']).all()
    assert carts['user_id'].isin(users['user_id']).all()
    assert orders['user_id'].isin(users['user_id']).all()

    # Связи продуктов
    assert cart_items['product_id'].isin(products['product_id']).all()

    # Связи корзин
    assert cart_items['cart_id'].isin(carts['cart_id']).all()
    assert orders['cart_id'].isin(carts['cart_id']).all()

    # Связи заказов и платежей
    paid_orders = orders[orders['status'] == 'delivered']['order_id']
    assert payments['order_id'].isin(paid_orders).all()

    print("Generating fake data complete\n")

    print('\n=== Generation Summary ===')
    print(f'Users:     {len(users)}')
    print(f'Products:  {len(products)}')
    print(f'Sessions:  {len(sessions)}  (avg {len(sessions) / len(users):.1f} per user)')
    print(f'Carts:     {len(carts)}    ({len(carts) / len(sessions) * 100:.1f}% of sessions)')
    print(f'Cart items:{len(cart_items)}  (avg {len(cart_items) / len(carts):.1f} per cart)')
    print(f'Orders:    {len(orders)}    ({len(orders) / len(carts) * 100:.1f}% of carts)')
    print(
        f'Payments:  {len(payments)}  ({len(payments) / len(orders[orders["status"] == "delivered"]) * 100 if len(orders[orders["status"] == "delivered"]) > 0 else 0:.1f}% of delivered orders)')
    print()

    # Save data in files
    print('Save data to csv files')
    users.to_csv(BASE_DIR / RAW_DATA_DIR / USERS_FILE, index=False)
    print(f'{USERS_FILE} saved. Count string: {len(users)}')

    products.to_csv(BASE_DIR / RAW_DATA_DIR / PRODUCTS_FILE, index=False)
    print(f'{PRODUCTS_FILE} saved. Count string: {len(products)}')

    sessions.to_csv(BASE_DIR / RAW_DATA_DIR / SESSIONS_FILE, index=False)
    print(f'{SESSIONS_FILE} saved. Count string: {len(sessions)}')

    carts.to_csv(BASE_DIR / RAW_DATA_DIR / CARTS_FILE, index=False)
    print(f'{CARTS_FILE} saved. Count string: {len(carts)}')

    cart_items.to_csv(BASE_DIR / RAW_DATA_DIR / CART_ITEMS_FILE, index=False)
    print(f'{CART_ITEMS_FILE} saved. Count string: {len(cart_items)}')

    orders.to_csv(BASE_DIR / RAW_DATA_DIR / ORDERS_FILE, index=False)
    print(f'{ORDERS_FILE} saved. Count string: {len(orders)}')

    payments.to_csv(BASE_DIR / RAW_DATA_DIR / PAYMENTS_FILE, index=False)
    print(f'{PAYMENTS_FILE} saved. Count string: {len(payments)}')


if __name__ == '__main__':
    main()