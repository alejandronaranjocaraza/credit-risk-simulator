import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import yaml
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=60000, key="autorefresh")
API_URL = "http://fastapi:8000"

# Get model name

with open('/config.yml', 'r') as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)

model_name = None
for name, cfg in config['models'].items():
    if cfg['active'] == True:
        model_name = name
        break

st.set_page_config(page_title="Credit Risk Dashboard", layout="wide")

# Model materics

st.header("Model Performance with Training Data")
st.markdown(f"Model: {model_name}")

try:
    response = requests.get(f"{API_URL}/metrics/{model_name}")
    metrics = response.json()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("AUC-ROC", round(metrics["auc"], 3))
    col2.metric("KS Statistic", round(metrics["ks"], 3))
    col3.metric("Precision (Default)", round(metrics["precision_pos"], 3))
    col4.metric("Precision (Non-Default)", round(metrics["precision_neg"], 3))
    col5.metric("Recall (Default)", round(metrics["recall_score_pos"], 3))

except Exception as e:
    st.error(f"Could not load metrics: {e}")

st.divider()

# Predictions data

st.header("Applicant Predictions")
st.markdown("Last 250 predictions")

try:
    response = requests.get(f"{API_URL}/predictions/250")
    data = response.json()

    if not data:
        st.warning("No predictions yet. Run the Airflow DAG first.")
        st.stop()

    df = pd.DataFrame(data)
    df["approved"] = df["approved"].map({True: "Approved", False: "Rejected"})

    # Summary
    total = len(df)
    approved = (df["approved"] == "Approved").sum()
    rejected = total - approved

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Applicants", total)
    col2.metric("Approved", approved)
    col3.metric("Rejected", rejected)

    st.divider()

    # Charts
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Approval by Sex")
        fig = px.histogram(
            df, x="sex", color="approved",
            barmode="group",
            color_discrete_map={"Approved": "#2ecc71", "Rejected": "#e74c3c"}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Approval by Housing")
        fig = px.histogram(
            df, x="housing", color="approved",
            barmode="group",
            color_discrete_map={"Approved": "#2ecc71", "Rejected": "#e74c3c"}
        )
        st.plotly_chart(fig, use_container_width=True)

    col_left2, col_right2 = st.columns(2)

    with col_left2:
        st.subheader("Approval by Purpose")
        fig = px.histogram(
            df, x="purpose", color="approved",
            barmode="group",
            color_discrete_map={"Approved": "#2ecc71", "Rejected": "#e74c3c"}
        )
        fig.update_layout(xaxis_tickangle=-30)
        st.plotly_chart(fig, use_container_width=True)

    with col_right2:
        st.subheader("Default Probability by Age")
        fig = px.histogram(
            df, x="age", color="approved",
            nbins=20,
            color_discrete_map={"Approved": "#2ecc71", "Rejected": "#e74c3c"}
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Raw data
    st.subheader("Raw Predictions")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Could not load predictions: {e}")
