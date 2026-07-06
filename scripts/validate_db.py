"""
Скрипт валидации данных, загруженных в PostgreSQL.
Проверяет:
- Количество строк > 0 во всех таблицах.
- Отсутствие "сирот" (записей, нарушающих внешние ключи).
- Соответствие сумм платежей и стоимости позиций заказов.
- Корректность статусов заказов и положительность цен.
- Уникальность первичных ключей (дополнительно).
"""

from sqlalchemy import create_engine, text

# Параметры подключения (те же, что и в load_to_db.py)
DB_USER = "postgres_user"
DB_PASSWORD = "postgres_password"
DB_HOST = "localhost"
DB_PORT = "5430"
DB_NAME = "postgres_db"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def check_table_not_empty(table_name: str) -> bool:
    """Проверяет, что таблица содержит хотя бы одну строку."""
    with engine.connect() as conn:
        count = conn.execute(
            text(f"SELECT COUNT(*) FROM {table_name}")
        ).scalar()
        assert count > 0, f"Таблица {table_name} пуста!"
        print(f"✔ {table_name}: {count} записей")

def check_no_orphans(child_table: str, child_column: str,
                     parent_table: str, parent_column: str) -> bool:
    """
    Проверяет, что все значения в child_table.child_column
    присутствуют в parent_table.parent_column.
    """
    with engine.connect() as conn:
        orphans = conn.execute(
            text(f"""
                SELECT COUNT(*)
                FROM {child_table} c
                LEFT JOIN {parent_table} p
                    ON c.{child_column} = p.{parent_column}
                WHERE p.{parent_column} IS NULL
            """)
        ).scalar()
        assert orphans == 0, (
            f"Найдено {orphans} записей в {child_table}.{child_column}, "
            f"отсутствующих в {parent_table}.{parent_column}!"
        )
        print(f"✔ Связь {child_table}.{child_column} -> {parent_table}.{parent_column}: OK")

def check_order_statuses() -> bool:
    """Проверяет, что статусы заказов принадлежат допустимому множеству."""
    with engine.connect() as conn:
        invalid = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM fct_orders
                WHERE status NOT IN ('delivered', 'cancelled')
            """)
        ).scalar()
        assert invalid == 0, f"Найдено {invalid} заказов с некорректным статусом!"
        print("✔ Статусы заказов: OK")

def check_positive_prices() -> bool:
    """Проверяет, что base_price в dim_products и amount в fct_payments > 0."""
    with engine.connect() as conn:
        bad_prices = conn.execute(
            text("SELECT COUNT(*) FROM dim_products WHERE base_price <= 0")
        ).scalar()
        assert bad_prices == 0, f"Найдено {bad_prices} товаров с неположительной ценой!"

        bad_amounts = conn.execute(
            text("SELECT COUNT(*) FROM fct_payments WHERE amount <= 0")
        ).scalar()
        assert bad_amounts == 0, f"Найдено {bad_amounts} платежей с неположительной суммой!"
        print("✔ Цены и суммы: OK")

def check_payment_amounts() -> bool:
    """
    Сравнивает сумму платежей с суммой стоимости позиций для доставленных заказов.
    """
    with engine.connect() as conn:
        discrepancy = conn.execute(
            text("""
                WITH order_sums AS (
                    SELECT
                        o.order_id,
                        SUM(ci.quantity * p.base_price) AS calculated_amount
                    FROM fct_orders o
                    JOIN fct_cart_items ci ON o.cart_id = ci.cart_id
                    JOIN dim_products p ON ci.product_id = p.product_id
                    WHERE o.status = 'delivered'
                    GROUP BY o.order_id
                )
                SELECT COUNT(*)
                FROM order_sums os
                JOIN fct_payments pay ON os.order_id = pay.order_id
                WHERE ABS(os.calculated_amount - pay.amount) > 0.01
            """)
        ).scalar()
        assert discrepancy == 0, (
            f"Найдено {discrepancy} платежей с суммой, не совпадающей с рассчитанной!"
        )
        print("✔ Суммы платежей соответствуют заказам")

def check_unique_keys() -> bool:
    """Проверяет уникальность первичных ключей в ключевых таблицах."""
    checks = [
        ("dim_users", "user_id"),
        ("dim_products", "product_id"),
        ("fct_sessions", "session_id"),
        ("fct_carts", "cart_id"),
        ("fct_orders", "order_id"),
        ("fct_payments", "payment_id"),
        # Для fct_cart_items уникальна пара (cart_id, cart_item_id)
    ]
    with engine.connect() as conn:
        for table, col in checks:
            duplicates = conn.execute(
                text(f"SELECT COUNT(*) FROM (SELECT {col} FROM {table} GROUP BY {col} HAVING COUNT(*) > 1) sub")
            ).scalar()
            assert duplicates == 0, f"Дубликаты в {table}.{col}!"
        # составной ключ для cart_items
        dup_cart_items = conn.execute(
            text("""
                SELECT COUNT(*) FROM (
                    SELECT cart_id, cart_item_id
                    FROM fct_cart_items
                    GROUP BY cart_id, cart_item_id
                    HAVING COUNT(*) > 1
                ) sub
            """)
        ).scalar()
        assert dup_cart_items == 0, "Дубликаты в fct_cart_items (cart_id, cart_item_id)!"
        print("✔ Уникальность первичных ключей: OK")

def main():
    print("Запуск валидации данных...\n")

    # 1. Все таблицы не пусты
    print("=== Проверка количества записей ===")
    for table in [
        "dim_users", "dim_products", "fct_sessions",
        "fct_carts", "fct_cart_items", "fct_orders", "fct_payments"
    ]:
        check_table_not_empty(table)

    # 2. Внешние ключи
    print("\n=== Проверка целостности связей ===")
    check_no_orphans("fct_sessions", "user_id", "dim_users", "user_id")
    check_no_orphans("fct_carts", "user_id", "dim_users", "user_id")
    check_no_orphans("fct_carts", "session_id", "fct_sessions", "session_id")
    check_no_orphans("fct_cart_items", "cart_id", "fct_carts", "cart_id")
    check_no_orphans("fct_cart_items", "product_id", "dim_products", "product_id")
    check_no_orphans("fct_orders", "user_id", "dim_users", "user_id")
    check_no_orphans("fct_orders", "cart_id", "fct_carts", "cart_id")
    check_no_orphans("fct_payments", "order_id", "fct_orders", "order_id")

    # 3. Статусы заказов
    print("\n=== Проверка бизнес-правил ===")
    check_order_statuses()
    check_positive_prices()
    check_payment_amounts()

    # 4. Уникальность ключей
    print("\n=== Проверка уникальности ключей ===")
    check_unique_keys()

    print("\n🎉 Все проверки пройдены успешно! Данные корректны.")

if __name__ == "__main__":
    main()