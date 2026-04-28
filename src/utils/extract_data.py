from sqlalchemy import create_engine
import pandas as pd

def extract_data(
        credentials: dict(),
        table_name: str(),
        columns: list()
):
    try:

        database = credentials['database']
        user = credentials['user']
        password = credentials['password']
        host = credentials['host']
        port = credentials['port']

    except:

        print("Error: Not all credentials specified")
        raise

    try:
        engine = create_engine(
            f"postgresql://{user}:{password}@{host}:{port}/{database}")
        query = "select "
        query += ",".join(columns)
        query += f" from {table_name};"

        data = pd.read_sql(query, engine)
        return data

    except Exception as err:
        print("Data import error: ", err)
        raise
