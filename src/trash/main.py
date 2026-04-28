from train_model import extract_data
from train_model import scale, one_hot_encode
from train_model import save_model, generate_model
from evaluate_model import load_model, model_predict, evaluate_model, save_to_json

from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from scipy.stats import ks_2samp

import pandas as pd
import numpy as np

database_credentials = {
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5433'
}
table_name = 'fct__german_credit_wide'
regression_cols = [
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
decision_tree_cols = [
    'risk',
    'age_numeric_group',
    'sex',
    'loan_term_numeric_tier',
    'saving_accounts',
    'checking_account',
    'has_no_savings_info',
    'has_no_checking_info',
    'job_skill_level',
    'housing',
    'purpose_risk_group'
]

target = 'risk'

# Create and save regression model
X, y = extract_data(database_credentials, table_name, regression_cols, target)
X_scaled = scale(X)
X_encoded = one_hot_encode(X_scaled)

X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

model = generate_model(X_train, y_train)
save_model(model, "../models/log-regression")
del model

# Create and save decision tree model
X, y = extract_data(database_credentials, table_name, decision_tree_cols, target)
encode_cols = ['sex', 'saving_accounts', 'checking_account', 'housing', 'purpose_risk_group']
X = pd.get_dummies(X, columns=encode_cols, drop_first=False).astype(int)
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)


thresh = 0.53
model = load_model("../models/log-regression")

y_prob, y_pred = model_predict(model, X_test, thresh)
metrics = evaluate_model(y_prob, y_pred, y_test)
save_to_json(metrics, "../models/log-regression.json")
