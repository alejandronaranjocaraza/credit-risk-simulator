# Credit Risk ML Pipeline Simulator

This repository provides an example of a machine learning pipeline to predict customer credit default based on the solicitor's general profile (for example, sex, age, housing and job skill level) and the credit application details (duration, loan amount). The pipeline uses past customer default histoy to train machine learning models, ingests simulated loan applications and calculates default probabilities per application. Finally, the pipeline classifies each new solicitor as "approved" / "not approved" for a given probability theshold.

Two ML models are used:
- Logistic regression
- Decision trees

Model parameters and selected features can be specified cleanly in .yaml files and, for the purposes of this project, each model, as well as parameter and feature selection is done beforehand with jupyter notebooks.

During each trainin faze, the pipeline does provide precision, recall, AUC-ROC score and KS statistic for each model given the chosen parameters and features.

This repository is designed primarily as a learning and documentation project.

## Objective

The goal is to combine
- Efficient data engineering
- Machine learning theory and implementation
- Python-based experimentation and visualization

## Models Used

- Logistic Regression
- Logistic Regression with sigmoid function callibration
- Decision Tree
- Decision Tree with sigmoid function callibration

## Technology Used

- PostgreSQL for data warehousing
- Docker Compose for full project containerization
- Apache Airflow for pipeline orchestration
- dbt for basic feature extraction, data cleaning and transofrmations
- scikit-learn for model training, evaluation and predictions
- FastAPI serves predictions and model evaluation metrics
- seaborn, plotly for visualization
- streamlit for dashboard

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
│   └── model.pkl
│   └── metrics.json
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Learning Objectives

This repository is designed primarily as a learning and documentation project focused on:

- Machine Leaning theory and scalable implementation with scikit-learn
- Postgres database adminstration and containerization through docker
- Airlow deployment and containerization
- Airflow DAG structuring
- Eficient and scalable dbt porject and SQL scripting
- API integration in python using FastAPI
- Basic dashboarding with streamlt

While at the time of building this I have experience with most of the tools used, this project
allowed to brush up on best-practices and delve deeper into the fundamentals.
For example, deploying a postgres server from scratch required a review of the server's internal database (also postgres), SQL injection to build initial framewrofk, adminstration of user privalages, etc.
Deploying the project from a docker-container required a review of databse exposure through local ports.

## References

- Reis, J., & Housley, M. (2022). *Fundamentals of Data Engineering.* O'Reilly.
  <https://soclibrary.futa.edu.ng/books/Fundamentals%20of%20Data%20Engineering%20(Reis,%20JoeHousley,%20Matt)%20(Z-Library).pdf>
- Obe, R., & Hsu, L. (n.d.). *PostgreSQL: Up and Running.* O'Reilly.
  <https://learning.oreilly.com/library/view/postgresql-up-and/9798341660885/ch01.html#sect2_pgAdmin>
- Müller, A. C., & Guido, S. (2016). *Introduction to Machine Learning with Python.* O'Reilly.
  <https://www.oreilly.com/library/view/introduction-to-machine/9781449369880/>
- Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly.
  <https://learning.oreilly.com/library/view/hands-on-machine-learning/9781491962282/>
- dbt Labs. (n.d.). *dbt Documentation.*
  <https://docs.getdbt.com/docs/introduction>
- PostgreSQL Global Development Group. (n.d.). *PostgreSQL Documentation.*
  <https://www.postgresql.org/docs/>
- dockerdocks. *Docker documentation*
  <https://docs.docker.com/>
- scikit-learn developers. (n.d.). *scikit-learn Documentation.*
  <http://scikit-learn.org/stable/>
- GeeksforGeeks. (n.d.). *GeeksforGeeks.*
  <https://www.geeksforgeeks.org/>
- DataCamp. (n.d.). *DataCamp.*
  <https://www.datacamp.com/>
