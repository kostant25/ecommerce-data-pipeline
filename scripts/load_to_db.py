from sqlalchemy import create_engine, text
import pandas as pd

from generator.config import BASE_DIR, RAW_DATA_DIR

db_engine = create_engine('postgresql://postgres_user:postgres_password@localhost:5430/postgres_db')
file_names = ['dim_users', 'dim_products', 'fct_sessions', 'fct_carts', 'fct_cart_items', 'fct_orders', 'fct_payments']
DATE_COLS = {
    'dim_users': ['registration_date'],
    'dim_products': [],                # нет дат
    'fct_sessions': ['start_time', 'end_time'],
    'fct_carts': ['created_time'],
    'fct_cart_items': ['added_time'],
    'fct_orders': ['order_time'],
    'fct_payments': ['payment_time']
}


def load_csv_to_db(file_name, engine, loading=True):
    parse_dates = DATE_COLS.get(file_name, [])
    table = pd.read_csv(BASE_DIR / RAW_DATA_DIR / f'{file_name}.csv', parse_dates=parse_dates)

    print(f'Количество строк в csv файле: {len(table)}')

    if loading:
        print(f'Начинаем загрузку {file_name} в БД...')

        table.to_sql(
            name=file_name,
            con=engine,
            if_exists='append',
            index=False
        )

        print(f'Загрузка {file_name} завершена')

        with engine.connect() as conn:
            count = conn.execute(text(f'SELECT COUNT(*) FROM {file_name}')).scalar()

            print(f'Загружено {count} из {len(table)} записей')
            print('================================')

            assert count == len(table), f'\nОшибка: вставлено {count}, ожидалось {len(table)}'


def clear_all_tables(engine):
    with engine.connect() as conn:
        for table in reversed(file_names):
            conn.execute(text(f"TRUNCATE TABLE {table} CASCADE"))
        conn.commit()
    print("All tables truncated.")


if __name__ == '__main__':
    isLoading = True
    clear_all_tables(db_engine)
    for name in file_names:
        load_csv_to_db(name, db_engine, loading=isLoading)