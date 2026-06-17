# 💳 Real-Time Credit Card Fraud Detection System

## Overview

This project is an end-to-end machine learning solution for detecting fraudulent credit card transactions in real time.

The system combines:

- Machine Learning
- FastAPI
- Dash
- SQLite
- Docker
- Kafka (streaming-ready)
- Plotly
- Python

It provides both operational fraud monitoring and executive analytics.

---

# Features

## Machine Learning

Multiple models evaluated:

- Random Forest
- Logistic Regression
- Naive Bayes
- XGBoost
- Support Vector Machine

Production model:

- Random Forest

---

## Real-Time Prediction API

Built using FastAPI.

Features:

- Transaction scoring
- Fraud probability calculation
- Risk classification
- Recommended actions
- Prediction storage

Swagger UI:

http://127.0.0.1:8000/docs

---

## Interactive Dashboard

Built using Dash and Plotly.

Includes:

- KPI cards
- Fraud risk gauge
- Fraud trend analysis
- Fraud heatmap
- Country exposure
- Merchant exposure
- Channel exposure
- Top risk countries
- Top merchants
- Fraud probability distribution
- Live fraud alerts
- Executive summary

---

# Architecture

Transaction Generator

↓

FastAPI API

↓

Machine Learning Model

↓

SQLite Database

↓

Dash Dashboard

↓

Executive Analytics

---

# Folder Structure

```text
credit_card_fraud_project
│
├── api/
├── dashboard/
├── database/
├── docker/
├── docs/
├── models/
├── models_other/
├── notebooks/
├── reports/
├── scripts/
├── simulator/
├── requirements.txt
└── README.md
```

---

# Machine Learning Models

| Model | Status |
|--------|--------|
| Random Forest | Production |
| Logistic Regression | Evaluated |
| Naive Bayes | Evaluated |
| XGBoost | Evaluated |
| SVM | Evaluated |

---

# Dashboard Components

### KPI Cards

- Fraud Alerts
- Genuine Transactions
- Fraud Exposure
- Fraud Rate

### Executive Analytics

- Risk Gauge
- Fraud Heatmap
- Top Risk Countries
- Top Merchants
- Fraud Trend
- Fraud Probability Histogram

### Operational Monitoring

- Latest Fraud Alerts
- Top 10 High Risk Transactions
- Hourly Summary

---

# Technology Stack

### Backend

- Python
- FastAPI

### Dashboard

- Dash
- Plotly

### Machine Learning

- Scikit-learn
- Pandas
- NumPy

### Database

- SQLite

### Containerization

- Docker

### Streaming

- Kafka (planned)

---

# Installation

Clone repository:

```bash
git clone https://github.com/madesina2025/credit_card_fraud_project.git
```

Activate environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Start API

```bash
uvicorn api.main:app --reload
```

---

# Start Dashboard

```bash
python dashboard/dash_app.py
```

Dashboard URL:

http://127.0.0.1:8050

---

# Documentation

Detailed documentation is available inside:

```text
docs/
```

Files:

- architecture.md
- api_documentation.md
- dashboard_guide.md
- deployment_guide.md

---

# Future Enhancements

- PostgreSQL
- Kafka Streaming
- Redis
- WebSocket
- Email Alerts
- SMS Alerts
- Grafana
- Prometheus
- AWS Deployment
- Azure Deployment
- GCP Deployment

---

# Author

Mukaila Adesina

Data Engineer | BI Developer | Machine Learning Enthusiast

GitHub:

https://github.com/madesina2025

