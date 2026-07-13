
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Konstantin',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'ecommerce_pipeline',
    default_args=default_args,
    description='Сквозной пайплайн: генерация данных и загрузка в PostgreSQL',
    schedule_interval='@daily',
    catchup=False,
    tags=['ecommerce', 'etl'],
) as dag:

    generate_task = BashOperator(
        task_id='generate_data',
        bash_command='python /opt/airflow/project/generator/generate.py',
    )

    load_task = BashOperator(
        task_id='load_to_db',
        bash_command='python /opt/airflow/project/scripts/load_to_db.py',
    )

    dbt_task = BashOperator(
        task_id='dbt_run',
        bash_command=(
            'cd /opt/airflow/project/dbt/ecommerce_analytics && '
            'dbt run --target docker --profiles-dir .'
        ),
    )

    generate_task >> load_task >> dbt_task