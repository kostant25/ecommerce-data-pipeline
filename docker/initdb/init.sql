-- База для Airflow
CREATE DATABASE airflow_db;
-- База для служебных данных Metabase
CREATE DATABASE metabaseappdb;
-- Пользователь для Metabase
CREATE USER metabase WITH PASSWORD 'mysecretpassword';
GRANT ALL PRIVILEGES ON DATABASE metabaseappdb TO metabase;
GRANT CONNECT ON DATABASE metabaseappdb TO metabase;