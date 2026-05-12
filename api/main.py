from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
from src.utils.feature_engineering import build_features
from src.utils.transform_data import one_hot_encode, scale
from src.utils.evaluate_model import model_predict
from psycopg2.extras import RealDictCursor

import json
import pickle
import yaml
import pandas as pd
import psycopg2


class Application(BaseModel):
    age: int
    sex: Literal[
        'male',
        'female'
    ]
    job: int
    housing: Literal[
        'own',
        'free',
        'rent'
    ]
    saving_accounts: Literal[
        'little',
        'moderate',
        'rich',
        'quite_rich',
        'NA'
    ]
    checking_account: Literal[
        'little',
        'moderate',
        'rich',
        'NA'
    ]
    credit_amount: int
    duration: int
    purpose: Literal[
        'car',
        'furniture/equipment',
        'radio/TV',
        'domestic appliances',
        'business',
        'education',
        'repairs',
    ]


app = FastAPI()

model = None
model_name = None
config = None


@app.on_event("startup")
def load_model():
    global model, model_name, config
    with open('/config.yml', 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    model_name = None
    for name, cfg in config['models'].items():
        if cfg['active'] == True:
            model_name = name
            break
    with open("/app/models/"+model_name+".pkl", "rb") as f:
        model = pickle.load(f)


@app.get("/metrics/{model_name}")
async def get_metrics(model_name: str):
    with open(f"/app/models/"+model_name+"-current.json", 'r') as f:
        data = json.load(f)
    return data


@app.post("/candidate")
async def check_application(application: Application):
    df = build_features(application.dict())
    cols = config['models'][model_name]['features']
    df = df[cols]
    threshold = config['models'][model_name]['threshold']

    # Transform data
    if 'scale' in config['models'][model_name]:
        scale_cols = config['models'][model_name]['scale']['features']
        df = scale(df, scale_cols)

    if 'one-hot' in config['models'][model_name]:
        encode_cols = config['models'][model_name]['one-hot']['features']
        drop_first = config['models'][model_name]['one-hot']['drop-first']
        df = one_hot_encode(df, encode_cols, drop_first)

    # Get feature columns (full)
    with open("/app/models/"+model_name+"_features.pkl", "rb") as f:
        feature_cols = pickle.load(f)

    df = df.reindex(columns=feature_cols, fill_value=0)

    y_prob, y_pred = model_predict(model, df, threshold)

    return {
        "default_probability": round(float(y_prob[0]), 4),
        "rating": round(float(1-y_prob[0]), 4),
        "approved": bool(y_pred[0])
    }


@app.get("/predictions")
async def get_predictions():
    conn = psycopg2.connect(
        host="warehouse-db",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="postgres"
    )
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        """
        SELECT
            id,
            age,
            sex,
            job,
            housing,
            saving_accounts,
            checking_account,
            credit_amount,
            duration,
            purpose,
            rating,
            approved,
            simulated_at
        FROM raw_applicants
        WHERE approved IS NOT NULL
        ORDER BY simulated_at DESC
        LIMIT 100;
        """
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return list(rows)
