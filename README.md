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
│ └── generate.py # Скрипт генерации
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

## 📈 План развития
 - Модель данных и конфигурация генератора
 - Реализация генератора синтетических данных
 - Staging‑слой и загрузка в PostgreSQL
 - Оркестрация пайплайна в Airflow
 - Трансформации dbt и построение витрин
 - Дашборд в BI‑инструменте
 - Документирование и публикация

## 📬 Контакты
  - Автор: Константин Панарин
  - Email: [goduskospan@gmail.com](mailto:goduskospan@gmail.com)
  - GitHub: https://github.com/kostant25
