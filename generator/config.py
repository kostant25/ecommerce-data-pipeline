# количество пользователей и товаров
NUM_USERS = 5000
NUM_PRODUCTS = 1000

# диапазоны дат
# регистрация
REGISTRATION_START = '2023-01-01'
REGISTRATION_END = '2024-06-30'

# ивенты - сессии, корзины, заказы, оплаты
EVENT_START = '2023-01-01'
EVENT_END = '2024-07-31'

# списки категорий и подкатегорий
CATEGORIES = [
    'Electronics',
    'Clothing',
    'Home & Garden',
    'Sports & Outdoors',
    'Beauty & Health',
    'Automotive',
    'Books & Hobbies',
    'Food',
    'Children\'s Goods',
    'Office & Stationery'
]
SUBCATEGORIES = {
    'Electronics': ['Smartphones', 'Laptops', 'Headphones', 'Tablets', 'Accessories'],
    'Clothing': ['T-Shirts', 'Jeans', 'Jackets', 'Dresses', 'Shoes'],
    'Home & Garden': ['Furniture', 'Lighting', 'Decor', 'Textiles', 'Garden Tools'],
    'Sports & Outdoors': ['Exercise Equipment', 'Sportswear', 'Camping', 'Bicycles', 'Yoga & Fitness'],
    'Beauty & Health': ['Skincare', 'Makeup', 'Fragrances', 'Vitamins', 'Hair Care'],
    'Automotive': ['Car Accessories', 'Oils & Fluids', 'Tyres', 'Car Electronics', 'Tools'],
    'Books & Hobbies': ['Books', 'Board Games', 'Musical Instruments', 'Crafts', 'Puzzles'],
    'Food': ['Beverages', 'Snacks', 'Groceries', 'Sweets', 'Canned Food'],
    'Children\'s Goods': ['Toys', 'Diapers', 'Kids\' Clothing', 'Feeding', 'Strollers'],
    'Office & Stationery': ['Paper & Notebooks', 'Pens & Pencils', 'Office Electronics', 'Office Furniture', 'Organizers']
}

# виды девайсов
DEVICE_TYPES = ['desktop', 'mobile', 'tablet']

# источники трафика
UTM_SOURCES = ['organic', 'google_ads', 'facebook_ads', 'direct', 'referral']

# вероятности
CART_CREATION_PROBABILITY = 0.3 # создание корзины в сессии
ORDER_PROBABILITY = 0.4         # оформление заказа
PAYMENT_PROBABILITY = 0.9       # оплата заказа

# мин макс цены товаров
PRICE_MEAN = 200
PRICE_STD = 100

# мин макс товаров в корзине (уникальных товаров)
CART_ITEM_MIN = 1
CART_ITEM_MAX = 5

# Название директории хранения сырых данных
RAW_DATA_DIR = 'data/raw'

# Названия файлов с сырыми данными
USERS_FILE = 'users.csv'
PRODUCTS_FILE = 'products.csv'
SESSIONS_FILE = 'sessions.csv'
CARTS_FILE = 'carts.csv'
CART_ITEMS_FILE = 'cart_items.csv'
ORDERS_FILE = 'orders.csv'
PAYMENTS_FILE = 'payments.csv'
