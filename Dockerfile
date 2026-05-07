FROM apache/airflow:3.2.1

RUN pip install --no-cache-dir \
    pandas \
    psycopg2-binary \
    sqlalchemy \
    dbt-core \
    dbt-postgres \
    scikit-learn
