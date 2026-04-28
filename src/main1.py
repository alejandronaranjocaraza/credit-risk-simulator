from utils.extract_data import extract_data
from utils.transform_data import scale
from utils.transform_data import one_hot_encode
from utils.build_models import build_log_regression
from utils.evaluate_model import model_predict, evaluate_model

from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from scipy.stats import ks_2samp

import pandas as pd
import numpy as np
import yaml
import pickle
import json

with open('config.yml', 'r') as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)

# Create and save regression model
credentials = config['source']
table = credentials.pop('model')
cols = config['models']['log-regression']['columns']
target = config['models']['log-regression']['target']
data = extract_data(credentials, table, cols)
y = data[target]
X = data.drop(target, axis=1, inplace=False)

# Transform data
scale_cols = config['models']['log-regression']['scale']
encode_cols = config['models']['log-regression']['one-hot-encode']

X = scale(X, scale_cols)
X = one_hot_encode(X, encode_cols)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# Build and train model
model = build_log_regression()
model.fit(X_train, y_train)

# Save model
with open(f"../models/log-regression.pkl", "wb") as f:
    pickle.dump(model, f)

# Evaluate model
threshold = config['models']['log-regression']['threshold']
y_prob, y_pred = model_predict(model, X_test, threshold)
metrics = evaluate_model(y_prob, y_pred, y_test)

# Save metrics
opts = {}
with open(f"../models/log-regression.json", "w") as f:
    json.dump(metrics, f, **opts)
