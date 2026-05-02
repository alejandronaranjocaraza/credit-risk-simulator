from src.credit_sim import simulate_applications
from datetime import datetime, timedelta, timezone
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import dag, task


@dag(
    schedule=timedelta(seconds=60),
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    default_args={"retries": 1, "retry_delay": timedelta(seconds=30)},
)
def simulate_credit_applications():

    @task()
    def get_data():
        data = simulate_applications()
        rows = list(zip(
            data["age"],
            data["sex"],
            data["job"],
            data["housing"],
            data["saving_accounts"],
            data["checking_account"],
            data["credit_amount"],
            data["duration"],
            data["purpose"],
        ))
        return rows

    @task()
    def insert_data(rows):
        hook = PostgresHook(postgres_conn_id="warehouse_db")
        hook.run(
            """
            CREATE TABLE IF NOT EXISTS credit_applications (
                id                  SERIAL PRIMARY KEY,
                age                 INT,
                sex                 TEXT,
                job                 INT,
                housing             TEXT,
                saving_accounts     TEXT,
                checking_account    TEXT,
                credit_amount       INT,
                duration            INT,
                purpose             TEXT,
                simulated_at        TIMESTAMP DEFAULT NOW(),
                rating              DECIMAL DEFAULT NULL,
                approved            BOOLEAN DEFAULT NULL
            )
            """
        )
        hook.insert_rows(
            table='credit_applications',
            rows=rows,
            target_fields=[
                'age', 'sex', 'job', 'housing', 'saving_accounts',
                'checking_account', 'credit_amount', 'duration', 'purpose'
            ]
        )

    applications = get_data()
    insert_data(applications)


simulate_credit_applications()
