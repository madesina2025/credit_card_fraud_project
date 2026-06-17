# System Architecture

## Overview

The Credit Card Fraud Detection System is a real-time machine learning solution designed to identify suspicious transactions and provide operational analytics through a dashboard.

The architecture combines:

- Machine Learning
- FastAPI
- SQLite Database
- Dash Dashboard
- Docker
- Real-Time Monitoring

---

# High-Level Architecture

```text
Transaction Generator
        │
        ▼
FastAPI Prediction API
        │
        ▼
Machine Learning Model
(Random Forest)
        │
        ▼
Fraud Prediction Output
        │
        ▼
SQLite Database
        │
        ▼
Dash Dashboard
        │
        ▼
Executive Analytics
```

---

# Components

## Transaction Generator

File:

simulator/transaction_generator.py

Purpose:

- Simulates live transactions
- Generates realistic transaction attributes
- Sends requests to FastAPI

---

## FastAPI Prediction Service

File:

api/main.py

Purpose:

- Accept incoming transactions
- Load trained model
- Generate predictions
- Calculate fraud probability
- Assign risk categories
- Store results in database

Endpoint:

POST /predict

---

## Machine Learning Layer

Files:

models/realistic_fraud_model.pkl

models/realistic_fraud_features.pkl

Purpose:

- Fraud prediction
- Probability scoring
- Binary classification

Current Production Model:

Random Forest

Other Models Evaluated:

- Logistic Regression
- Naive Bayes
- SVM
- XGBoost

---

## Database Layer

Current:

SQLite

Future:

PostgreSQL

Purpose:

- Store predictions
- Provide dashboard source
- Support analytics queries

Main Table:

fraud_predictions

---

## Dashboard Layer

File:

dashboard/dash_app.py

Purpose:

Real-time visualization and executive reporting.

Contains:

- Fraud KPIs
- Risk Gauge
- Fraud Trend
- Fraud Heatmap
- Fraud Exposure
- Top Countries
- Top Merchants
- Alert Feed
- Fraud Probability Distribution
- Executive Summary

Refresh Rate:

5 seconds

---

# Current Data Flow

```text
Transaction Generator
        ↓
FastAPI API
        ↓
Random Forest Model
        ↓
SQLite Database
        ↓
Dash Dashboard
        ↓
Executive Analytics
```

---

# Fraud Decision Flow

```text
Transaction
      ↓
Feature Processing
      ↓
Random Forest Model
      ↓
Fraud Probability
      ↓
Risk Category
      ↓
Recommended Action
      ↓
Database
      ↓
Dashboard
```

---

# Risk Categories

Critical

Probability ≥ 0.90

Action:

Flag for fraud review / possible block

---

High

Probability ≥ 0.70

Action:

Manual review

---

Medium

Probability ≥ 0.40

Action:

Monitor

---

Low

Probability < 0.40

Action:

Approve

---

# Dashboard Analytics

### Operational Metrics

- Total Transactions
- Fraud Count
- Genuine Count
- Fraud Rate

### Risk Metrics

- Fraud Exposure
- Risk Gauge
- Top Risk Countries
- Top Merchants

### Real-Time Monitoring

- Alert Feed
- Trend Over Time
- Heat Map
- Fraud Distribution

---

# Containerization

Docker Components

```text
Docker Container
      │
      ├── FastAPI
      ├── Dash Dashboard
      ├── SQLite Database
      └── Python Environment
```

---

# Future Architecture

```text
Transaction Generator
        ↓
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
        ↓
Email Alerts
        ↓
SMS Alerts
```

---

# Cloud Deployment Targets

AWS

Services:

- EC2
- ECS
- RDS PostgreSQL
- S3

Azure

Services:

- Azure Container Apps
- Azure PostgreSQL
- Azure Monitor

GCP

Services:

- Cloud Run
- Cloud SQL
- BigQuery

---

# Monitoring

Future tools:

- Grafana
- Prometheus
- ELK Stack

---

# Author

Mukaila Adesina

Data Engineer | BI Developer | Machine Learning Enthusiast

GitHub:

https://github.com/madesina2025

