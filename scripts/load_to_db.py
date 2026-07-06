import sys
from pathlib import Path

from psycopg2 import extras

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine, text
import pandas as pd

from generator.config import BASE_DIR, RAW_DATA_DIR

db_engine = create_engine('postgresql://postgres_user:postgres_password@postgres:5432/postgres_db')
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

        conn = engine.raw_connection()
        try:
            with conn.cursor() as cur:
                # Формируем список кортежей
                tuples = [tuple(x) for x in table.to_numpy()]
                cols = ','.join(list(table.columns))
                query = f"INSERT INTO {file_name} ({cols}) VALUES %s"
                extras.execute_values(cur, query, tuples)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

        print(f'Загрузка {file_name} завершена')

        with engine.begin() as conn:
            count = conn.execute(text(f'SELECT COUNT(*) FROM {file_name}')).scalar()

            print(f'Загружено {count} из {len(table)} записей')
            print('================================')

            assert count == len(table), f'\nОшибка: вставлено {count}, ожидалось {len(table)}'


def clear_all_tables(engine):
    with engine.begin() as conn:
        for table in reversed(file_names):
            conn.execute(text(f"TRUNCATE TABLE {table} CASCADE"))
    print("All tables truncated.")


if __name__ == '__main__':
    isLoading = True
    clear_all_tables(db_engine)
    for name in file_names:
        load_csv_to_db(name, db_engine, loading=isLoading)