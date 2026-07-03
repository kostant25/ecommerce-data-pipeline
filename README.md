# E-commerce Data Pipeline

Сквозной проект по построению аналитического конвейера для интернет‑магазина: от генерации синтетических данных до визуализации бизнес‑метрик.

## 🎯 Цель
Создать максимально приближенный к реальности ETL/ELT-пайплайн, который включает:
- **Генератор синтетических данных** (пользователи, сессии, корзины, заказы, платежи)
- **Оркестрацию** (Apache Airflow)
- **Трансформации** (dbt)
- **Визуализацию** (Metabase / Yandex DataLens)

Проект выполняется в рамках подготовки к позиции **Junior+/Middle Data Engineer / Analytics Engineer**.

## 🛠️ Стек
- Python 3 (Faker, Pandas, NumPy)
- PostgreSQL
- Docker, Docker Compose
- Apache Airflow
- dbt Core
- Metabase (или аналог)
- Git, GitHub

## 📁 Структура репозитория
```
ecommerce-data-pipeline/
├── generator/ # Генератор синтетических данных
│ ├── init.py
│ ├── config.py # Конфигурация и параметры
│ ├── generate.py # Скрипт генерации
│ ├── dimensions.py
│ └── facts.py
├── data/
│ └── raw/ # Сгенерированные CSV (игнорируются Git)
├── docker/ # Docker Compose для инфраструктуры
├── sql/ # DDL и аналитические запросы
├── README.md
├── requirements.txt
└── .gitignore
```
## 🚀 Быстрый старт (генератор)

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/<your-username>/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline
```

### 2. Настройте виртуальное окружение
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Установите зависимости
```bash
pip install -r requirements.txt
```

### 4. Запустите генератор
```bash
python generator/generate.py
```

Скрипт создаст CSV‑файлы в папке ```data/raw/``` (файлы исключены из Git).

### Генератор
Генератор создаёт реалистичные синтетические данные с соблюдением логики воронки:
- Сессии не пересекаются по времени у одного пользователя.
- Корзины создаются с заданной вероятностью, внутри сессии.
- Каждый товар в корзине уникален, добавляется случайное количество.
- Заказы создаются на основе корзин, с возможностью отмены.
- Платежи генерируются только для доставленных заказов, сумма рассчитывается из цен товаров.

В процессе генерации выполняются проверки уникальности ключей и внешних связей. Для воспроизводимости зафиксированы seed'ы.

### ⚙️ Настройка генерации
Все параметры (количество пользователей, товаров, вероятности конверсии, диапазоны дат) находятся в файле `generator/config.py`. Измените их по необходимости перед запуском `generate.py`.

## 📈 План развития
- [x] Модель данных и конфигурация генератора
- [x] Реализация генератора синтетических данных
- [ ] Staging‑слой и загрузка в PostgreSQL
- [ ] Оркестрация пайплайна в Airflow
- [ ] Трансформации dbt и построение витрин
- [ ] Дашборд в BI‑инструменте
- [ ] Документирование и публикация

## 📊 Схема данных
Сгенерированные таблицы и их основные поля:

- **dim_users** – пользователи (user_id, name, email, registration_date, city, state)
- **dim_products** – товары (product_id, product_name, category, subcategory, base_price)
- **fct_sessions** – сессии пользователей на сайте (session_id, user_id, start_time, end_time, device_type, utm_source)
- **fct_carts** – корзины (cart_id, user_id, session_id, created_time)
- **fct_cart_items** – товары в корзинах (cart_id, cart_item_id, product_id, quantity, added_time)
- **fct_orders** – заказы (order_id, user_id, cart_id, order_time, status)
- **fct_payments** – платежи (payment_id, order_id, amount, payment_time, method)

Связи: users → sessions → carts → orders → payments; carts → cart_items ← products.

## 📬 Контакты
  - Автор: Константин Панарин
  - Email: [goduskospan@gmail.com](mailto:goduskospan@gmail.com)
  - GitHub: https://github.com/kostant25
