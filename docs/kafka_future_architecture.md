# Future Streaming Architecture

## Overview

The current solution uses:

Transaction Generator → FastAPI → SQLite → Dash Dashboard

The next evolution of the platform will introduce Kafka streaming, PostgreSQL, Grafana, and Prometheus to support enterprise-scale fraud detection.

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
FastAPI Scoring Engine
        ↓
PostgreSQL Database
        ↓
Dash Dashboard
        ↓
Grafana Monitoring
        ↓
Prometheus Metrics
```

---

# Components

## Transaction Generator

Generates realistic banking transactions.

Examples:

- Customer ID
- Merchant
- Country
- Channel
- Amount

Source:

```text
simulator/transaction_generator.py
```

---

## Kafka Producer

Publishes transactions into Kafka topics.

Future file:

```text
simulator/kafka_producer.py
```

Responsibilities:

- Real-time streaming
- Event publishing
- High throughput

---

## Kafka Topic

Acts as message broker.

Topic:

```text
fraud_transactions
```

Purpose:

- Decouple producer and consumer
- Handle large transaction volumes
- Improve scalability

---

## Kafka Consumer

Consumes messages and forwards them to the prediction engine.

Future file:

```text
simulator/kafka_consumer.py
```

Responsibilities:

- Message processing
- Batch consumption
- Fault tolerance

---

## FastAPI Scoring Engine

Current file:

```text
api/main.py
```

Responsibilities:

- Load trained Random Forest model
- Score transactions
- Generate fraud probabilities
- Assign risk categories

Risk Categories:

- Low
- Medium
- High
- Critical

---

## PostgreSQL Database

Future replacement for SQLite.

Advantages:

- Scalability
- ACID compliance
- Better concurrency
- Production ready

Tables:

- predictions
- alerts
- audit_logs

---

## Dash Dashboard

Current file:

```text
dashboard/dash_app.py
```

Provides:

- Fraud Risk Gauge
- Heatmap
- Trend Analysis
- Top Countries
- Top Merchants
- Executive Summary
- Live Alerts

---

## Grafana Monitoring

Future addition.

Provides:

- Real-time metrics
- Dashboards
- Alerting

Metrics:

- Transactions/sec
- Fraud rate
- API latency
- Database health

---

## Prometheus

Future addition.

Responsibilities:

- Metrics collection
- Monitoring
- Alert rules

Metrics:

- CPU
- Memory
- API requests
- Kafka throughput

---

# Future Cloud Deployments

## AWS

Services:

- EC2
- ECS
- RDS PostgreSQL
- MSK Kafka
- CloudWatch

---

## Azure

Services:

- Azure VM
- Azure Database for PostgreSQL
- Event Hub
- Azure Monitor

---

## GCP

Services:

- Compute Engine
- Cloud SQL
- Pub/Sub
- Monitoring

---

# Target Enterprise Architecture

```text
Producer
   ↓
Kafka
   ↓
Consumer
   ↓
FastAPI
   ↓
PostgreSQL
   ↓
Dash Dashboard
   ↓
Grafana + Prometheus
```

---

# Benefits

- Real-time streaming
- High availability
- Horizontal scalability
- Monitoring and observability
- Production readiness
- Enterprise architecture

---

# Author

Mukaila Adesina

Data Engineer | BI Developer | Machine Learning Enthusiast

GitHub:

https://github.com/madesina2025

