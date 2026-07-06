CREATE TABLE IF NOT EXISTS dim_users (
    user_id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) NOT NULL UNIQUE,
    registration_date TIMESTAMP NOT NULL,
    city VARCHAR(100),
    state VARCHAR(2)
);

CREATE TABLE IF NOT EXISTS dim_products (
    product_id VARCHAR(32) PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    base_price NUMERIC(10,2) NOT NULL CHECK (base_price > 0)
);

CREATE TABLE IF NOT EXISTS fct_sessions (
    session_id VARCHAR(32) PRIMARY KEY,
    user_id VARCHAR(32) REFERENCES dim_users(user_id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    device_type VARCHAR(20) NOT NULL,
    utm_source VARCHAR(50) NOT NULL,
    CHECK (end_time >= start_time)
);

CREATE TABLE IF NOT EXISTS fct_carts (
    cart_id VARCHAR(32) PRIMARY KEY,
    user_id VARCHAR(32) REFERENCES dim_users(user_id),
    session_id VARCHAR(32) REFERENCES fct_sessions(session_id),
    created_time TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS fct_cart_items (
    cart_id VARCHAR(32) REFERENCES fct_carts(cart_id),
    cart_item_id SMALLINT NOT NULL,
    product_id VARCHAR(32) REFERENCES dim_products(product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    added_time TIMESTAMP NOT NULL,
    PRIMARY KEY (cart_id, cart_item_id)
);

CREATE TABLE IF NOT EXISTS fct_orders (
    order_id VARCHAR(32) PRIMARY KEY,
    user_id VARCHAR(32) REFERENCES dim_users(user_id),
    cart_id VARCHAR(32) REFERENCES fct_carts(cart_id) UNIQUE,
    order_time TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('delivered', 'cancelled'))
);

CREATE TABLE IF NOT EXISTS fct_payments (
    payment_id VARCHAR(32) PRIMARY KEY,
    order_id VARCHAR(32) REFERENCES fct_orders(order_id) UNIQUE,
    amount NUMERIC(10,2) NOT NULL CHECK (amount > 0),
    payment_time TIMESTAMP NOT NULL,
    method VARCHAR(20) NOT NULL
);