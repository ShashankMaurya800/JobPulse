FROM apache/airflow:3.1.0

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

RUN pip install --no-cache-dir \
    pandas==2.3.3 \
    openpyxl \
    SQLAlchemy \
    psycopg2-binary \
    python-dotenv