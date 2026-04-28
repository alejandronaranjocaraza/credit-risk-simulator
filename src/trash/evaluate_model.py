from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import roc_auc_score
from scipy.stats import ks_2samp

import pickle
import json


def load_model(directory: str()):
    with open(directory+".pkl", "rb") as f:
        res = pickle.load(f)
    return res


def model_predict(model, X_test, thresh):
    y_prob = model.predict_proba(X_test)[:, 1]
    y_pred = (y_prob >= thresh).astype(int)
    return y_prob, y_pred


def evaluate_model(y_prob, y_pred, y_test):
    precision_pos = precision_score(
        y_test,
        y_pred,
        average='binary', pos_label=1
    )
    precision_neg = precision_score(
        y_test,
        y_pred,
        average='binary', pos_label=0
    )
    recall_score_pos = recall_score(
        y_test,
        y_pred,
        average='binary', pos_label=1
    )
    recall_score_neg = recall_score(
        y_test,
        y_pred,
        average='binary', pos_label=0
    )
    auc = roc_auc_score(y_test, y_prob)
    good = y_prob[y_test == 0]
    bad = y_prob[y_test == 1]
    ks, _ = ks_2samp(good, bad)
    res = {
        'auc': auc,
        'ks': ks,
        'precision_pos': precision_pos,
        'precision_neg': precision_neg,
        'recall_score_pos': recall_score_pos,
        'recall_score_neg': recall_score_neg
    }
    return res


def save_to_json(dic: dict(), directory: str(), options={}):
    with open(directory, "w") as f:
        json.dump(dic, f, **options)
