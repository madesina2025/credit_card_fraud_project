# Architecture Guide

# Real-Time Credit Card Fraud Detection System

---

# Solution Overview

The solution simulates a real-world fraud detection platform used by banks and financial institutions.

It consists of:

1. Transaction Generator
2. Prediction API
3. Machine Learning Model
4. Database Layer
5. Dashboard Layer
6. Executive Analytics
7. Alert Engine
8. Kafka Streaming Components (Prepared)
9. Docker Deployment

---

# High-Level Architecture

```text
                 Transaction Generator
                           │
                           ▼
                  FastAPI Prediction API
                           │
                           ▼
                 Random Forest ML Model
                           │
                           ▼
                  Fraud Probability Score
                           │
                           ▼
                     SQLite Database
                           │
        ┌──────────────────┴──────────────────┐
        ▼                                     ▼
  Executive Dashboard                    Alert Feed
        │
        ▼
 Real-Time Fraud Monitoring
```

---

# Component Architecture

## Transaction Simulator

Location:

```
simulator/
```

Files:

```
transaction_generator.py
kafka_producer.py
kafka_consumer.py
```

Responsibilities:

- Generate realistic transactions
- Simulate customer activity
- Produce transaction streams
- Support Kafka streaming architecture

---

## FastAPI Layer

Location:

```
api/main.py
```

Responsibilities:

- Receive transactions
- Load trained model
- Perform inference
- Return fraud probability
- Store prediction results

Endpoints:

```
POST /predict

GET /predictions

GET /health
```

---

## Machine Learning Layer

Location:

```
models/
```

Production Model:

```
realistic_fraud_model.pkl
```

Features:

```
realistic_fraud_features.pkl
```

Alternative models:

```
models_other/
```

Contains:

- Logistic Regression
- Naive Bayes
- SVM
- XGBoost

Responsibilities:

- Predict fraud probability
- Classify transaction risk
- Support model comparison

---

## Database Layer

Location:

```
database/
```

Files:

```
db.py
models.py
```

Database:

SQLite

Stores:

- Transaction details
- Fraud probability
- Risk category
- Recommended action
- Timestamp

---

## Dashboard Layer

Location:

```
dashboard/
```

Main file:

```
dash_app.py
```

Built using:

- Dash
- Plotly
- Plotly Express

Provides:

Real-time fraud monitoring and executive analytics.

---

# Dashboard Architecture

```text
                 SQLite Database
                         │
                         ▼
                Dash Callback Engine
                         │
 ┌──────────────┬──────────────┬───────────────┐
 ▼              ▼              ▼
KPIs        Visual Charts     Alert Feed
```

---

# Executive Summary Layer

Provides:

### Total Transactions

### Critical Alerts

### High Alerts

### Medium Alerts

### Low Alerts

---

# Exposure Analytics

Provides:

### Fraud Exposure by Merchant

### Fraud Exposure by Country

### Fraud Exposure by Channel

### Top 5 Risk Countries

### Top 5 Merchants

---

# Trend Analytics

Provides:

### Fraud Trend Over Time

### Fraud Heat Map by Hour

### Hourly Fraud Table

---

# Executive Analytics

Provides:

### Risk Gauge

### Fraud Probability Histogram

### Live Alert Feed

### Alert Ticker

### Executive Summary Panel

---

# Data Flow

```text
Transaction Generator
        │
        ▼
FastAPI Endpoint
        │
        ▼
Random Forest Model
        │
        ▼
Fraud Probability
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

# Machine Learning Pipeline

```text
Raw Dataset
     │
     ▼
Preprocessing
     │
     ▼
Train/Test Split
     │
     ▼
Model Training
     │
     ▼
Model Evaluation
     │
     ▼
Pickle Serialization
     │
     ▼
Production Deployment
```

---

# Docker Architecture

```text
               Docker Container
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
    FastAPI        Dashboard      SQLite
```

---

# Streaming Architecture (Prepared)

```text
Transaction Producer
          │
          ▼
       Kafka Topic
          │
          ▼
     Kafka Consumer
          │
          ▼
      Fraud Model
          │
          ▼
        Database
          │
          ▼
      Dashboard
```

---

# Future Architecture

```text
Customer Transactions
        │
        ▼
Kafka
        │
        ▼
Spark Streaming
        │
        ▼
Random Forest Model
        │
        ▼
PostgreSQL
        │
        ▼
Dashboard
        │
        ▼
Grafana
        │
        ▼
Email / SMS Alerts
```

---

# Technologies Used

## Machine Learning

- Scikit-Learn
- Random Forest
- Logistic Regression
- Naive Bayes
- XGBoost

## API

- FastAPI
- Uvicorn

## Dashboard

- Dash
- Plotly

## Database

- SQLite

## Containerization

- Docker

## Streaming

- Kafka

## Language

- Python

---

# Author

Mukaila Adesina

Data Engineer | BI Developer | Machine Learning Enthusiast

GitHub:

https://github.com/madesina2025
