# Credit Card Fraud Detection System

## Overview

This project is an end-to-end Credit Card Fraud Detection platform that combines Machine Learning, Real-Time Transaction Monitoring, API Services, PostgreSQL, Docker and Interactive Dashboards.

The solution simulates live financial transactions, scores them using a trained fraud detection model and visualizes fraud activity in real time.

---

## Architecture

Transaction Generator
↓
Fraud Detection API (FastAPI)
↓
Machine Learning Model
↓
PostgreSQL Database
↓
Dash Dashboard
↓
Real-Time Monitoring

---

## Features

- Fraud Prediction API
- Random Forest Fraud Model
- Live Transaction Simulator
- PostgreSQL Integration
- Dockerized Deployment
- Real-Time Fraud Dashboard
- Fraud by Merchant
- Fraud by Country
- Risk Score Monitoring
- Fraud Alerts

---

## Technology Stack

### Backend

- Python
- FastAPI
- PostgreSQL

### Machine Learning

- Scikit-Learn
- Random Forest
- Pandas
- NumPy

### Dashboard

- Dash
- Plotly

### DevOps

- Docker
- Docker Compose
- GitHub

---

## Project Structure

```text
credit_card_fraud_project/

├── api/
│   └── main.py

├── database/
│   ├── db.py
│   └── models.py

├── models/
│   └── random_forest_fraud_model.pkl

├── simulator/
│   ├── transaction_generator.py
│   ├── kafka_producer.py
│   └── kafka_consumer.py

├── dash_app.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Running Locally

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start API

```bash
uvicorn api.main:app --reload
```

### Start Dashboard

```bash
python dash_app.py
```

---

## Dashboard

The dashboard provides:

- Fraud Alerts
- Fraud Count by Merchant
- Fraud Count by Country
- Transaction Monitoring
- Risk Level Analysis

---

## Future Enhancements

- Kafka Streaming
- AWS Deployment
- Azure Deployment
- Real-Time Alert Notifications
- Power BI Integration
- Tableau Integration

---

## Author

Mukaila Adesina

Data Engineer | Data Scientist | BI Developer

GitHub:
https://github.com/madesina2025