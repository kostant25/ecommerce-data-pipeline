FROM python:3.12-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc && \
    python -m venv /opt/venv
COPY requirements.txt /requirements.txt
RUN /opt/venv/bin/pip install --no-cache-dir -r /requirements.txt && \
    /opt/venv/bin/pip install --no-cache-dir sqlalchemy==1.4.52

FROM apache/airflow:2.10.5
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
USER airflow