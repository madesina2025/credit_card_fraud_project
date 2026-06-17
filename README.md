# 🚨 Real-Time Credit Card Fraud Detection Platform

An end-to-end fraud detection platform that combines Machine Learning, FastAPI, PostgreSQL, Kafka Streaming, Docker, and Dash Analytics to detect, monitor, and analyze fraudulent credit card transactions in real time.

The solution provides both operational fraud monitoring and executive-level fraud analytics through a modern dashboard and API-driven architecture.

---

# 📌 Project Overview

Financial institutions process millions of transactions daily, making fraud detection a critical business requirement.

This platform provides:

- Real-time transaction scoring
- Fraud probability prediction
- Fraud risk classification
- Fraud alert generation
- Fraud exposure analysis
- Executive fraud dashboards
- Streaming-ready architecture
- Enterprise deployment readiness

---

# 🏗 Solution Architecture

```text
Transaction Simulator
         │
         ▼
      FastAPI
         │
         ▼
 Machine Learning Model
 (Random Forest)
         │
         ▼
 PostgreSQL Database
         │
         ▼
 Executive Dashboard
      (Dash)
```

Future Architecture:

```text
Transaction Simulator
         │
         ▼
   Kafka Producer
         │
         ▼
       Kafka
         │
         ▼
   Kafka Consumer
         │
         ▼
      FastAPI
         │
         ▼
 Machine Learning Model
         │
         ▼
 PostgreSQL Database
         │
         ▼
 Executive Dashboard
```

---

# ⚙️ Technology Stack

## Machine Learning

- Python
- Scikit-Learn
- Pandas
- NumPy

## API Layer

- FastAPI
- Uvicorn

## Dashboard & Analytics

- Dash
- Plotly

## Database

- PostgreSQL
- SQLite (Development)

## Streaming

- Apache Kafka
- Kafka Producer
- Kafka Consumer

## Containerization

- Docker
- Docker Compose

## Cloud Ready

- AWS
- Azure
- GCP

---

# 🤖 Machine Learning Models Evaluated

The following models were trained and evaluated:

- Random Forest
- Logistic Regression
- Naive Bayes
- Support Vector Machine (SVM)
- XGBoost

### Production Model

✅ Random Forest Classifier

Selected due to its strong balance of:

- Accuracy
- Recall
- Precision
- Fraud detection capability

---

# 📊 Project Metrics

Dataset:

- 284,807 Transactions
- 492 Fraud Cases

Performance Highlights:

- Accuracy: ~99.9%
- High Recall Performance
- High Precision Performance
- Optimized for Fraud Detection

---

# 🚀 Real-Time Prediction API

Built using FastAPI.

Features:

- Transaction Scoring
- Fraud Probability Calculation
- Risk Classification
- Recommended Actions
- Prediction Storage

### Local Swagger Documentation

```text
http://127.0.0.1:8000/docs
```

Available after starting the FastAPI service locally.

---

# 📈 Executive Dashboard

Built using Dash and Plotly.

Provides real-time fraud monitoring and executive analytics.

## Executive KPI Cards

- Total Transactions
- Fraud Alerts
- Genuine Transactions
- Fraud Exposure
- Average Fraud Probability

## Fraud Monitoring

- Fraud Risk Gauge
- Fraud Trend Analysis
- Fraud Heatmap by Hour
- Fraud Probability Distribution
- Fraud Alert Feed

## Exposure Analytics

- Fraud Exposure by Country
- Fraud Exposure by Merchant
- Fraud Exposure by Channel

## Executive Intelligence

- Top 5 Risk Countries
- Top 5 Merchants
- Hourly Fraud Summary
- Executive Summary Panel
- Suspicious Transaction Review

---

# 🎯 Risk Classification Framework

| Probability | Risk Level | Action |
|------------|------------|---------|
| ≥ 0.90 | Critical | Block Transaction |
| ≥ 0.70 | High | Manual Review |
| ≥ 0.40 | Medium | Monitor |
| < 0.40 | Low | Approve |

---

# 🗄 Database Layer

The platform stores scored transactions for analytics and audit purposes.

Key Stored Fields:

- Transaction ID
- Customer
- Merchant
- Country
- Channel
- Amount
- Fraud Probability
- Risk Level
- Recommended Action
- Prediction Timestamp

Database:

- PostgreSQL
- Analytics-ready schema
- Dashboard integration

---

# 🔄 Kafka Streaming Components

Current Components:

- Kafka Producer
- Kafka Consumer
- Streaming Simulation Layer

Purpose:

- Real-time transaction ingestion
- Event-driven processing
- Scalable fraud monitoring

---

# 📂 Project Structure

```text
credit_card_fraud_project/
│
├── api/
│   └── main.py
│
├── dashboard/
│   └── dash_app.py
│
├── database/
│   ├── db.py
│   └── models.py
│
├── docker/
│   ├── docker-compose.yml
│   └── entrypoint.sh
│
├── simulator/
│   ├── transaction_generator.py
│   ├── kafka_producer.py
│   └── kafka_consumer.py
│
├── models/
│   ├── realistic_fraud_model.pkl
│   └── realistic_fraud_features.pkl
│
├── scripts/
│   ├── train_realistic_fraud_model.py
│   └── generate_flags.py
│
├── docs/
│
├── notebooks/
│
├── reports/
│
└── README.md
```

---

# 📚 Project Documentation

Detailed project documentation is available in the `/docs` folder.

| Document | Description |
|-----------|-------------|
| docs/architecture.md | Solution Architecture |
| docs/system_architecture.md | End-to-End Architecture |
| docs/api_documentation.md | FastAPI Documentation |
| docs/dashboard_guide.md | Dashboard Guide |
| docs/dashboard_features.md | Dashboard Features |
| docs/database_schema.md | Database Design |
| docs/model_documentation.md | ML Model Documentation |
| docs/business_case.md | Business Value |
| docs/project_structure.md | Folder Structure |
| docs/installation_guide.md | Installation Guide |
| docs/deployment_guide.md | Deployment Guide |
| docs/aws_deployment.md | AWS Deployment |
| docs/azure_deployment.md | Azure Deployment |
| docs/gcp_deployment.md | GCP Deployment |
| docs/kafka_future_architecture.md | Kafka Roadmap |
| docs/future_roadmap.md | Future Enhancements |

---

# 🔧 Installation

Clone repository:

```bash
git clone https://github.com/madesina2025/credit_card_fraud_project.git
cd credit_card_fraud_project
```

Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶ Start FastAPI

```bash
uvicorn api.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# ▶ Start Dashboard

```bash
python dashboard/dash_app.py
```

Dashboard:

```text
http://127.0.0.1:8050
```

---

# 🐳 Docker Deployment

```bash
docker compose up --build
```

Services:

- FastAPI
- PostgreSQL
- Dashboard

---

# 💼 Business Value

This solution supports:

- Fraud Operations
- Risk Analytics
- Financial Crime Monitoring
- Executive Reporting
- Operational Intelligence

Benefits:

- Faster Fraud Detection
- Reduced Financial Loss
- Improved Decision Making
- Real-Time Monitoring
- Enterprise Scalability

---

# 🔮 Future Enhancements

- Redis Cache
- WebSocket Streaming
- Email Alerts
- SMS Alerts
- Grafana Monitoring
- Prometheus Metrics
- Kubernetes Deployment
- Terraform Infrastructure
- AWS Production Deployment
- Azure Production Deployment
- GCP Production Deployment

---

# 👨‍💻 Author

**Mukaila Adesina**

Data Engineer | BI Developer | Machine Learning Enthusiast

GitHub:

https://github.com/madesina2025

---
