from utils.extract_data import extract_data
from utils.transform_data import scale
from utils.transform_data import one_hot_encode
from utils.build_models import build_model
from utils.evaluate_model import model_predict, evaluate_model

from sklearn.model_selection import train_test_split

import pandas as pd
import yaml
import pickle
import json

with open('config.yml', 'r') as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)

model_name = 'log-regression-cv'

# Create and save regression model
credentials = config['source']
table = credentials.pop('model')
cols = config['models'][model_name]['columns']
target = config['models'][model_name]['target']
data = extract_data(credentials, table, cols)
y = data[target]
X = data.drop(target, axis=1, inplace=False)

# Transform data
if 'scale' in config['models'][model_name]:
    scale_cols = config['models'][model_name]['scale']['columns']
    X = scale(X, scale_cols)

if 'one-hot' in config['models'][model_name]:
    encode_cols = config['models'][model_name]['one-hot']['columns']
    drop_first = config['models'][model_name]['one-hot']['drop-first']
    X = one_hot_encode(X, encode_cols, drop_first)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# Build and train model
model = build_model(model_name)
model.fit(X_train, y_train)

# Save model
with open("../models/"+model_name+".pkl", "wb") as f:
    pickle.dump(model, f)

# Evaluate model
threshold = config['models'][model_name]['threshold']
y_prob, y_pred = model_predict(model, X_test, threshold)
metrics = evaluate_model(y_prob, y_pred, y_test)

# Save metrics
date_str = pd.to_datetime('today').strftime('%Y%m%d')
opts = {}
with open(f"../models/"+model_name+"-"+date_str+".json", "w") as f:
    json.dump(metrics, f, **opts)
