# API Documentation

# Credit Card Fraud Detection API

---

## Overview

This API provides fraud prediction services for credit card transactions.

The API receives transaction details, performs machine learning inference, classifies transaction risk, stores the prediction, and exposes results for dashboard monitoring.

---

# Base URL



http://127.0.0.1:8000


---

# Framework

FastAPI

Swagger UI:



http://127.0.0.1:8000/docs


---

# Endpoints

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | /health | Health Check |
| POST | /predict | Fraud Prediction |
| GET | /predictions | Retrieve Stored Predictions |

---

# GET /health

## Purpose

Checks whether the API is running.

## Example

```bash
curl http://127.0.0.1:8000/health
Response
{
  "status":"ok"
}
POST /predict
Purpose

Predict whether a transaction is fraudulent.

Example Request
{
  "customer_id":"CUST123",
  "merchant":"Amazon",
  "country":"UK",
  "channel":"Online",
  "amount":3572.86,
  "hour_of_day":14,
  "transactions_last_hour":10,
  "days_since_account_open":20,
  "failed_login_attempts":3,
  "device_trust_score":0.35
}
Example Response
{
  "fraud_probability":0.9931,
  "prediction":1,
  "risk_label":"Fraud",
  "risk_category":"Critical",
  "recommended_action":"Flag for fraud review / possible block"
}
GET /predictions

Returns prediction records stored inside the database.

Risk Categories
Fraud ProbabilityRisk Category
>= 0.90Critical
0.70 - 0.89High
0.40 - 0.69Medium
< 0.40Low
Prediction Workflow

Request

↓

Input Validation

↓

Feature Engineering

↓

Model Prediction

↓

Fraud Probability

↓

Risk Classification

↓

Database Storage

↓

Dashboard Visualisation

Features Used
amount
hour_of_day
transactions_last_hour
days_since_account_open
failed_login_attempts
device_trust_score
Run API
uvicorn api.main:app --reload

Swagger Documentation:

http://127.0.0.1:8000/docs
Example Python Client
import requests

payload = {
    "customer_id":"CUST123",
    "merchant":"Amazon",
    "country":"UK",
    "channel":"Online",
    "amount":3572.86,
    "hour_of_day":14,
    "transactions_last_hour":10,
    "days_since_account_open":20,
    "failed_login_attempts":3,
    "device_trust_score":0.35
}

response = requests.post(
    "http://127.0.0.1:8000/predict",
    json=payload
)

print(response.json())
Operational Use Cases
Banking fraud monitoring
AML systems
FinTech applications
Fraud operations teams
Risk analytics
Internal control systems
Author

Mukaila Adesina

Data Engineer | BI Developer | Machine Learning Enthusiast

GitHub:

https://github.com/madesina2025

