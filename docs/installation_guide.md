# Installation Guide

# Credit Card Fraud Detection System

---

# Prerequisites

Ensure the following are installed:

- Python 3.9+
- pip
- Git
- Docker Desktop (optional)
- VS Code (recommended)

---

# Clone Repository

```bash
git clone https://github.com/madesina2025/credit_card_fraud_project.git

cd credit_card_fraud_project
```

---

# Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Mac/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Project Structure

```text
api/
dashboard/
database/
docs/
models/
notebooks/
reports/
scripts/
simulator/
```

---

# Start FastAPI

```bash
python api/main.py
```

Default URL:

http://127.0.0.1:8000

Swagger Documentation:

http://127.0.0.1:8000/docs

---

# Start Dashboard

```bash
python dashboard/dash_app.py
```

Dashboard URL:

http://127.0.0.1:8050

---

# Run Transaction Generator

```bash
python simulator/transaction_generator.py
```

Purpose:

Simulates real-time transactions.

---

# Docker Deployment

Build container:

```bash
docker compose up --build
```

Stop containers:

```bash
docker compose down
```

---

# Machine Learning Models

Located inside:

```text
models/
```

Current Production Model:

- realistic_fraud_model.pkl

Supporting Features:

- realistic_fraud_features.pkl

---

# Database

Current:

SQLite

Location:

```text
database/fraud.db
```

Future:

PostgreSQL

---

# Dashboard Refresh

Refresh Interval:

5 seconds

Source:

SQLite Database

---

# Main Components

FastAPI

↓

Random Forest Model

↓

SQLite Database

↓

Dash Dashboard

---

# Troubleshooting

## Port 8000 already in use

Kill process:

```bash
lsof -i :8000
kill -9 PID
```

---

## Port 8050 already in use

```bash
lsof -i :8050
kill -9 PID
```

---

## Module Not Found

Reinstall dependencies:

```bash
pip install -r requirements.txt
```

---

## Virtual Environment Problems

Deactivate:

```bash
deactivate
```

Activate:

```bash
source venv/bin/activate
```

---

# Future Improvements

- Kafka Streaming
- PostgreSQL
- Redis
- WebSockets
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

