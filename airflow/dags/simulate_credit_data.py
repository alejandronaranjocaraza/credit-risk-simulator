from src.credit_sim import simulate_applications
from src.utils.evaluate_model import model_predict
from src.utild.transform_data import scale, one_hot_encode
from datetime import datetime, timedelta, timezone
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sdk import dag, task
import subprocess
import yaml
import pickle


@dag(
    schedule=timedelta(seconds=60),
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    default_args={"retries": 1, "retry_delay": timedelta(seconds=30)},
)
def simulate_credit_applications():

    @task()
    def simulate_data():
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
        hook.insert_rows(
            table='raw_applicants',
            rows=rows,
            target_fields=[
                'age', 'sex', 'job', 'housing', 'saving_accounts',
                'checking_account', 'credit_amount', 'duration', 'purpose'
            ]
        )

    @task()
    def dbt_run():
        result = subprocess.run(
            ["dbt", "run",
             "--project-dir", "/opt/dbt",
             "--profiles-dir", "/opt/dbt"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print(result.stderr)
        if result.returncode != 0:
            raise Exception(f"dbt run failed:\n{result.stderr}")

    @task()
    def evaluate_data():
        # Get config
        with open('/opt/airflow/config.yml', 'r') as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)

        # Get model name
        model_name = None
        for model in config['models'].keys():
            if config['models'][model]['active'] == True:
                model_name = model
                break

        # Get threshold
        threshold = config['models'][model_name]['threshold']

        # Get columns
        cols = config['models'][model_name]['columns']

        # Get data
        hook = PostgresHook(postgres_conn_id="warehouse_db")
        df = hook.get_pandas_df(
                """
                select * from fet__applicants
                where rating is null or approved is null;
                """
        )
        if df.empty:
            print("No unscored rows found, skipping.")
            return
        X = df[cols]

        if 'scale' in config['models'][model_name]:
            scale_cols = config['models'][model_name]['scale']['columns']
            X = scale(X, scale_cols)

        if 'one-hot' in config['models'][model_name]:
            encode_cols = config['models'][model_name]['one-hot']['columns']
            drop_first = config['models'][model_name]['one-hot']['drop-first']
            X = one_hot_encode(X, encode_cols, drop_first)

        # Get model
        with open("/opt/airflow/models/"+model_name+".pkl", "rb") as f:
            model = pickle.load(f)

        y_prob, y_pred = model_predict(model, X, threshold)

        df['approved'] = y_pred.astype(bool)
        df['rating'] = y_prob

        hook.run(
                """
                update raw_applicants
                set rating = data.rating,
                    approved = data.approved
                FROM (VALUES %s) AS data(id, rating, approved)
                WHERE raw_applicants.id = data.id;
                """,
                parameters=list(zip(df['id'], df['rating'], df['approved']))
                )

    applications = simulate_data()
    insert_task = insert_data(applications)
    dbt_task = dbt_run()
    score_task = evaluate_data()
    insert_task >> dbt_task >> score_task


simulate_credit_applications()
