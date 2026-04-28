from sqlalchemy import create_engine
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import StratifiedKFold

from sklearn.calibration import CalibratedClassifierCV


def scale(df, columns):
    numeric = list(df.select_dtypes(include=['number']).columns)
    scaler = StandardScaler()
    numeric_scaled = scaler.fit_transform(df[numeric])
    df_scaled = df.copy()
    df_scaled[numeric] = numeric_scaled
    return df_scaled


def one_hot_encode(df):
    non_numeric = list(df.select_dtypes(exclude=['number']).columns)
    df_encoded = pd.get_dummies(
        df, columns=non_numeric, drop_first=True).astype(int)
    return df_encoded


def extract_data(
        credentials: dict(),
        table_name: str(),
        columns: list(),
        target: str()
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
        X = data.drop(columns=target, inplace=False)

        y = data[target]
        return X, y

    except Exception as err:
        print("Data import error: ", err)
        raise


def generate_model(X_train, y_train):

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    model = LogisticRegressionCV(
        l1_ratios=(1,),
        solver='saga',
        cv=cv,
        scoring='roc_auc',
        class_weight='balanced',
        max_iter=1000,
        use_legacy_attributes=False
    )
    calibrated_model = CalibratedClassifierCV(model, method='sigmoid')
    calibrated_model.fit(X_train, y_train)

    return calibrated_model


def save_model(model, directory: str()):
    with open(directory+".pkl", "wb") as f:
        pickle.dump(model, f)


def main():
    database_credentials = {
        'database': 'postgres',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': '5433'
    }
    table_name = 'fct__german_credit_wide'
    cols = [
        'risk',
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
    ]
    target = 'risk'
    X, y = extract_data(database_credentials, table_name, cols, target)
    X_scaled = scale(X)
    X_encoded = one_hot_encode(X_scaled)
    model = generate_model(X_encoded, y)
    save_model(model, "../models/log-regression")


main()
