from utils.evaluate_model import evaluate_model, model_predict

import yaml
import json
import pickle

with open('config.yml', 'r') as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)

model_name = "log_regression"
threshold = config['models'][model_name]['threshold']

with open("models/"+model_name+".pkl", "rb") as f:
    model = pickle.load(f)

# Extract new data
X_test = None
y_test = None

# Evaluate model
y_prob, y_pred = model_predict(model, X_test, threshold)
metrics = evaluate_model(y_prob, y_pred, y_test)

# Save metrics
opts = {}
with open(f"../models/"+model_name+".json", "w") as f:
    json.dump(metrics, f, **opts)
