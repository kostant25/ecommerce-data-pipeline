FROM apache/airflow:2.10.5
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt && \
    pip install --no-cache-dir sqlalchemy==1.4.52