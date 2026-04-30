# Credit Default ML Scoring Pipeline

**Work in Progress** — This project is currently under active development and does not yet run end-to-end.

This repository provides an example of a machine learning pipeline to predict customer credit default based on the applicant's general profile (e.g. sex, age, housing, and job skill level) and credit application details (duration and loan amount). The pipeline uses past customer default history to train machine learning models, ingests simulated loan applications, and calculates default probabilities per application. Finally, the pipeline classifies each new applicant as "approved" or "not approved" given a probability threshold.

## Dataset

The project uses the [Statlog German Credit dataset](https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data), a classic benchmark dataset containing 1,000 past loan applicants classified as good or bad credit risks. Each record includes demographic information (sex, age, housing, job skill level) and credit application details (duration, loan amount), making it well suited for binary credit default classification.

## Approach

The pipeline trains two ML models on the historical dataset:
- Logistic Regression
- Decision Tree

Both models are also calibrated using a sigmoid function to produce better-calibrated probability outputs. Model parameters and selected features are specified in `.yaml` files. Model selection, parameter tuning, and feature selection are done beforehand using Jupyter notebooks.

During each training phase, the pipeline outputs precision, recall, AUC-ROC score, and KS statistic for each model given the chosen parameters and features.

New loan applications are simulated and scored through an Apache Airflow DAG, which orchestrates applicant generation, feature extraction, and model scoring. Each applicant is assigned a default probability and classified as "approved" or "not approved" given a configurable threshold. Predictions and model evaluation metrics are served via a FastAPI endpoint and visualized through a Streamlit dashboard.

## Technology Used

- **PostgreSQL** for data warehousing
- **Docker Compose** for full project containerization
- **Apache Airflow** for pipeline orchestration
- **dbt** for feature extraction, data cleaning, and transformations
- **scikit-learn** for model training, evaluation, and predictions
- **FastAPI** for serving predictions and model evaluation metrics
- **seaborn** and **plotly** for visualization
- **Streamlit** for dashboarding

## Repository Structure

```text
│
├── data/
│   └── raw/
│       └── german_credit.csv
│
├── dbt_project/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── models/
│       ├── staging/
│       │   └── stg_credit_data.sql
│       ├── marts/
│       │   └── mart_credit_base.sql
│       └── features/
│           └── features_credit.sql
│
├── src/
│   ├── train_model.py
│   ├── evaluate_model.py
│   └── feature_engineering.py  ← shared logic, used by scoring too
│
├── airflow/
│   ├── dags/
│   │   └── scoring_pipeline.py
│   └── tasks/
│       ├── generate_applicants.py
│       └── score_applicants.py
│
├── api/
│   └── main.py
│
├── models/
│   ├── model.pkl
│   └── metrics.json
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Learning Objectives

This repository is designed primarily as a learning and documentation project focused on:
- Machine learning theory and scalable implementation with scikit-learn
- PostgreSQL database administration and containerization with Docker
- Airflow deployment and containerization
- Airflow DAG structuring
- Efficient and scalable dbt project and SQL scripting
- API integration in Python using FastAPI
- Basic dashboarding with Streamlit

While at the time of building this I had experience with most of the tools used, this project allowed me to brush up on best practices and delve deeper into the fundamentals. For example, deploying a PostgreSQL server from scratch required a review of the server's internal database, SQL scripting to build the initial framework, and administration of user privileges. Deploying the project from a Docker container required a review of database exposure through local ports.

## References

- Reis, J., & Housley, M. (2022). *Fundamentals of Data Engineering.* O'Reilly.<br>
  <https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/>
- Obe, R., & Hsu, L. (n.d.). *PostgreSQL: Up and Running.* O'Reilly.<br>
  <https://learning.oreilly.com/library/view/postgresql-up-and/9798341660885/ch01.html#sect2_pgAdmin>
- Müller, A. C., & Guido, S. (2016). *Introduction to Machine Learning with Python.* O'Reilly.<br>
  <https://www.oreilly.com/library/view/introduction-to-machine/9781449369880/>
- Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly.<br>
  <https://learning.oreilly.com/library/view/hands-on-machine-learning/9781491962282/>
- *dbt Documentation.*<br>
  <https://docs.getdbt.com/docs/introduction>
- *PostgreSQL Documentation.*<br>
  <https://www.postgresql.org/docs/>
- *Docker documentation*<br>
  <https://docs.docker.com/>
- *scikit-learn Documentation.*<br>
  <http://scikit-learn.org/stable/>
- *GeeksforGeeks.*<br>
  <https://www.geeksforgeeks.org/>
- *DataCamp.*<br>
  <https://www.datacamp.com/>
