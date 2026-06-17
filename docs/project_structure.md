# Project Structure

## Directory Layout

```text
credit_card_fraud_project
│
├── api
│   └── main.py
│
├── dashboard
│   ├── dash_app.py
│   ├── assets
│   ├── screenshots
│   ├── flagged_transactions_backup.csv
│   └── flagged_transactions_old.csv
│
├── data
│   ├── raw
│   ├── processed
│   ├── database
│   ├── creditcard.csv
│   ├── X_train.csv
│   ├── X_test.csv
│   ├── y_train.csv
│   └── y_test.csv
│
├── database
│   ├── db.py
│   └── models.py
│
├── docs
│   ├── architecture.md
│   ├── api_documentation.md
│   ├── dashboard_guide.md
│   ├── deployment_guide.md
│   ├── database_schema.md
│   └── README_images
│
├── docker
│   ├── docker-compose.yml
│   └── entrypoint.sh
│
├── models
│   ├── realistic_fraud_model.pkl
│   ├── realistic_fraud_features.pkl
│   └── random_forest_fraud_model.pkl
│
├── models_other
│   ├── logistic_regression_fraud_model.pkl
│   ├── naive_bayes_fraud_model.pkl
│   ├── support_vector_machine_fraud_model.pkl
│   └── xgboost_fraud_model.pkl
│
├── notebooks
│   └── CreditcardFraud_ML.ipynb
│
├── reports
│   ├── metrics
│   ├── confusion_matrices
│   ├── formatted_model_scores.csv
│   └── model_performance_with_table.png
│
├── scripts
│   ├── generate_flags.py
│   └── train_realistic_fraud_model.py
│
├── simulator
│   ├── transaction_generator.py
│   ├── kafka_producer.py
│   └── kafka_consumer.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Folder Responsibilities

## api/

Contains FastAPI application responsible for serving fraud predictions.

Files:

- main.py

Purpose:

- REST API
- Model inference
- Prediction endpoint

---

## dashboard/

Contains the Dash dashboard.

Features:

- Executive dashboard
- Real-time charts
- Fraud heatmap
- Risk gauge
- Alert ticker
- Top countries
- Top merchants
- Trend analysis

Main file:

- dash_app.py

---

## data/

Contains raw and processed datasets.

Includes:

- Original Kaggle dataset
- Train/Test splits
- Processed files
- Database storage

---

## database/

Contains database configuration.

Files:

- db.py
- models.py

Purpose:

- Database connection
- ORM models
- Table definitions

---

## models/

Stores production machine learning models.

Current production model:

- realistic_fraud_model.pkl

Supporting files:

- realistic_fraud_features.pkl

---

## models_other/

Stores experimental models.

Includes:

- Logistic Regression
- Naive Bayes
- SVM
- XGBoost

Purpose:

Model comparison.

---

## notebooks/

Contains exploratory notebooks.

File:

CreditcardFraud_ML.ipynb

Purpose:

- EDA
- Feature engineering
- Model training
- Evaluation

---

## reports/

Stores output artifacts.

Includes:

- Metrics
- Confusion matrices
- Performance charts
- CSV summaries

---

## scripts/

Utility scripts.

Examples:

- Model training
- Fraud flag generation

---

## simulator/

Generates synthetic transactions.

Includes:

transaction_generator.py

Future components:

- Kafka producer
- Kafka consumer

Purpose:

Simulate real-time transactions.

---

## docker/

Docker deployment files.

Includes:

- docker-compose.yml
- entrypoint.sh

Purpose:

Containerized deployment.

---

## docs/

Project documentation.

Contains:

- Architecture
- API guide
- Dashboard guide
- Deployment guide
- Database schema

---

# Data Flow

Transaction Generator

↓

FastAPI API

↓

ML Model

↓

Database

↓

Dash Dashboard

↓

Analytics

---

# Future Architecture

Kafka Producer

↓

Kafka Topic

↓

Kafka Consumer

↓

Fraud Prediction Service

↓

PostgreSQL

↓

Dash Dashboard

↓

Grafana

↓

Prometheus

---

# Author

Mukaila Adesina

Data Engineer | BI Developer | Machine Learning Enthusiast

GitHub:

https://github.com/madesina2025

