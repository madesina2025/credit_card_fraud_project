# GCP Deployment Guide

## Overview

The platform can be deployed on Google Cloud Platform.

---

# Architecture

```text
Transaction Generator
        ↓
FastAPI
        ↓
Random Forest Model
        ↓
Cloud SQL PostgreSQL
        ↓
Dash Dashboard
        ↓
Cloud Monitoring
```

---

# GCP Services

## Compute Engine

Hosts:

- FastAPI
- Dash

---

## Cloud SQL

Stores:

- Predictions
- Alerts
- Transactions

---

## Pub/Sub

Future streaming platform.

Equivalent to Kafka.

---

## Cloud Monitoring

Provides:

- Metrics
- Logging
- Alerts

---

## Artifact Registry

Stores Docker images.

---

## GKE

Runs Kubernetes containers.

Benefits:

- High availability
- Scalability

---

## Cloud Storage

Stores:

- Models
- Reports
- Screenshots

---

# Security

- IAM
- VPC
- Secrets Manager
- Firewall Rules

---

# Monitoring

Tracks:

- CPU
- Memory
- Requests
- API latency

---

# Author

Mukaila Adesina

GitHub:

https://github.com/madesina2025

