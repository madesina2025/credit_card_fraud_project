# Deployment Guide

# Credit Card Fraud Detection System

## Overview

This document describes how to run and deploy the entire Credit Card Fraud Detection project.

Components include:

- FastAPI prediction API
- Dash dashboard
- SQLite database
- Machine learning model
- Transaction simulator
- Kafka producer
- Kafka consumer
- Docker environment

---

## Project Requirements

Software required:

- Python 3.9+
- pip
- virtualenv
- Docker Desktop
- Git
- VS Code

---

# Local Setup

Navigate to the project folder:

```bash
pwd
```

Activate virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Start FastAPI

Run:

```bash
uvicorn api.main:app --reload
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

---

# Start Dashboard

Open another terminal.

Activate environment:

```bash
source venv/bin/activate
```

Run dashboard:

```bash
python dashboard/dash_app.py
```

Dashboard URL:

```text
http://127.0.0.1:8050
```

---

# Run Transaction Generator

Open another terminal.

Execute:

```bash
python simulator/transaction_generator.py
```

Purpose:

Generate live transactions continuously.

---

# Run Kafka Producer

```bash
python simulator/kafka_producer.py
```

---

# Run Kafka Consumer

```bash
python simulator/kafka_consumer.py
```

---

# Database

Current database:

SQLite

Files:

```text
database/db.py
database/models.py
```

Stores:

- Customer
- Merchant
- Country
- Channel
- Amount
- Fraud Probability
- Risk Category
- Recommended Action
- Timestamp

---

# Machine Learning Models

Location:

```text
models/
```

Files:

```text
realistic_fraud_model.pkl
realistic_fraud_features.pkl
random_forest_fraud_model.pkl
```

Additional models:

```text
models_other/
```

Includes:

- Logistic Regression
- Naive Bayes
- XGBoost
- SVM

---

# Docker Deployment

Location:

```text
docker/
```

Start containers:

```bash
docker compose -f docker/docker-compose.yml up --build
```

Stop containers:

```bash
docker compose -f docker/docker-compose.yml down
```

---

# Project Architecture

Transaction Generator

↓

FastAPI

↓

Machine Learning Model

↓

SQLite Database

↓

Dash Dashboard

↓

Executive Analytics

---

# Recommended Production Architecture

Transaction Source

↓

Kafka

↓

FastAPI

↓

ML Model

↓

PostgreSQL

↓

Dash Dashboard

↓

Alert Layer

↓

Monitoring

---

# Cloud Deployment

## AWS

Services:

- ECS
- EKS
- RDS PostgreSQL
- MSK Kafka
- S3
- CloudWatch

---

## Azure

Services:

- Container Apps
- Azure PostgreSQL
- Event Hubs
- Blob Storage
- Application Insights

---

## GCP

Services:

- Cloud Run
- Cloud SQL
- Pub/Sub
- Cloud Storage

---

# CI/CD Pipeline

GitHub

↓

GitHub Actions

↓

Docker Build

↓

Tests

↓

Container Registry

↓

Cloud Deployment

---

# Troubleshooting

## API Problems

Run:

```bash
uvicorn api.main:app --reload
```

---

## Dashboard Problems

Run:

```bash
python dashboard/dash_app.py
```

Dashboard URL:

```text
http://127.0.0.1:8050
```

---

## Missing Model

Check:

```bash
ls models
```

Expected:

```text
realistic_fraud_model.pkl
realistic_fraud_features.pkl
```

---

## Database Errors

Check:

```bash
ls database
```

Expected:

```text
db.py
models.py
```

---

# Future Improvements

- PostgreSQL migration
- Kafka streaming
- Redis cache
- Authentication
- Rate limiting
- Email alerts
- SMS alerts
- WebSocket updates
- Grafana monitoring
- Prometheus metrics
- AWS deployment
- Azure deployment
- GCP deployment

---

# Author

Mukaila Adesina

Data Engineer | BI Developer | Machine Learning Enthusiast

GitHub:

https://github.com/madesina2025

