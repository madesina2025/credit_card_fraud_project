# Model Documentation

# Credit Card Fraud Detection Machine Learning Model

---

# Overview

This document describes the machine learning models, training process, evaluation metrics, and production deployment approach used for fraud detection.

Current production model:

Random Forest

Purpose:

Identify fraudulent credit card transactions and assign fraud probabilities.

---

# Dataset

Source:

Kaggle Credit Card Fraud Dataset

Statistics:

- Total Records: 284,807
- Fraud Cases: 492
- Genuine Cases: 284,315

Class Distribution:

Highly Imbalanced

Fraud Percentage:

0.172%

---

# Data Preparation

Steps performed:

1. Missing value check
2. Duplicate removal
3. Feature engineering
4. Train/Test split
5. SMOTE oversampling
6. Model training
7. Model evaluation
8. Model serialization

---

# Feature Engineering

Features used:

### Transaction Features

- amount
- hour_of_day
- transactions_last_hour

### Customer Behaviour Features

- days_since_account_open
- failed_login_attempts

### Device Features

- device_trust_score

---

# Train/Test Split

Training Data:

80%

Testing Data:

20%

Random State:

42

---

# Handling Class Imbalance

Technique:

SMOTE

Purpose:

Generate synthetic minority samples.

Benefits:

- Improved recall
- Reduced false negatives
- Better fraud detection

---

# Models Evaluated

## Logistic Regression

Advantages:

- Fast
- Interpretable

Limitations:

- Linear assumptions

---

## Naive Bayes

Advantages:

- Lightweight
- Fast

Limitations:

- Feature independence assumption

---

## Support Vector Machine

Advantages:

- High accuracy

Limitations:

- Slow on large datasets

---

## XGBoost

Advantages:

- Powerful ensemble method

Limitations:

- Higher complexity

---

## Random Forest

Advantages:

- Robust
- Handles non-linear relationships
- Resistant to overfitting
- Fast inference

Chosen as production model.

---

# Evaluation Metrics

Metrics used:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC AUC

---

# Confusion Matrix

Measures:

True Positive

True Negative

False Positive

False Negative

Purpose:

Evaluate classification performance.

---

# ROC Curve

Purpose:

Measure model discrimination capability.

Metric:

AUC Score

Higher AUC indicates better performance.

---

# Production Model

Location:

models/

Files:

realistic_fraud_model.pkl

realistic_fraud_features.pkl

random_forest_fraud_model.pkl

Purpose:

Used by FastAPI prediction service.

---

# Prediction Workflow

Transaction

↓

Feature Engineering

↓

Random Forest Model

↓

Fraud Probability

↓

Risk Category

↓

Recommended Action

↓

Database Storage

↓

Dashboard Analytics

---

# Risk Categories

Critical

Fraud Probability ≥ 0.90

Action:

Flag for fraud review / possible block

---

High

Fraud Probability ≥ 0.70

Action:

Manual review

---

Medium

Fraud Probability ≥ 0.40

Action:

Monitor transaction

---

Low

Fraud Probability < 0.40

Action:

Approve transaction

---

# Feature Importance

Important drivers include:

- Amount
- Device Trust Score
- Failed Login Attempts
- Transactions Last Hour
- Account Age
- Hour of Day

---

# Strengths

- High accuracy
- Good recall
- Fast prediction speed
- Suitable for real-time systems
- Resistant to overfitting

---

# Limitations

- SQLite backend
- Simulated transaction source
- No concept drift monitoring
- No online learning

---

# Future Improvements

### Explainability

SHAP

LIME

---

### Monitoring

Model drift detection

Feature drift detection

---

### Infrastructure

PostgreSQL

Kafka

Redis

---

### Models

XGBoost

LightGBM

Neural Networks

---

### MLOps

MLflow

Airflow

CI/CD

Model Registry

---

# Current Architecture

Transaction

↓

FastAPI

↓

Random Forest

↓

SQLite

↓

Dash Dashboard

---

# Future Architecture

Kafka

↓

Streaming Prediction

↓

PostgreSQL

↓

Dashboard

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

