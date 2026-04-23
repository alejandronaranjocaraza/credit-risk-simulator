from sqlalchemy import create_engine
import pandas as pd


def extract_data():

    database = 'postgres'
    user = 'postgres'
    password = 'postgres'
    host = 'localhost'
    port = '5433'

    engine = create_engine(
        f"postgresql://{user}:{password}@{host}:{port}/{database}")
    query = "select * from fct__german_credit_wide"

    data = pd.read_sql(query, engine)
    data.drop(columns='id', inplace=True)

    X = data[[
        'sex',
        'credit_exposure',
        'loan_term_tier',
        'savings_score',
        'checking_score',
        'has_no_savings_info',
        'has_no_checking_info',
        'job_skill_level',
        'housing_stability_score',
        'purpose_risk_group'
    ]]

    y = data['risk']

    return X, y
