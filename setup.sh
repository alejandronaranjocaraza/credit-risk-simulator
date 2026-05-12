#!/bin/bash

echo "Starting all services..."
docker compose up -d

echo "Waiting for warehouse-db to be healthy..."
until docker compose exec warehouse-db pg_isready -U postgres > /dev/null 2>&1; do
    echo "  waiting..."
    sleep 2
done
echo "warehouse-db is ready."

echo "Waiting for airflow-worker to be healthy..."
until docker compose exec airflow-worker echo "ready" > /dev/null 2>&1; do
    echo "  waiting..."
    sleep 2
done
echo "airflow-worker ready."

echo "Running dbt..."
docker compose exec airflow-worker dbt run --project-dir /opt/dbt --profiles-dir /opt/dbt

echo "Training models..."
docker compose exec airflow-worker python /opt/airflow/dags/src/train_models.py

echo "Done. Everything is ready."
echo "Airflow: http://localhost:8080"
echo "FastAPI: http://localhost:8000/docs"
