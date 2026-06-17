# Azure Deployment Guide

## Overview

The solution can be deployed on Microsoft Azure.

---

# Architecture

```text
Transaction Generator
        ↓
FastAPI
        ↓
Random Forest Model
        ↓
Azure PostgreSQL
        ↓
Dash Dashboard
        ↓
Azure Monitor
```

---

# Azure Services

## Azure VM

Hosts:

- FastAPI
- Dash Dashboard

---

## Azure Database for PostgreSQL

Stores:

- Transactions
- Predictions
- Alerts

---

## Event Hub

Future streaming platform.

Equivalent to Kafka.

---

## Azure Monitor

Provides:

- Metrics
- Logs
- Alerts

---

## Azure Container Registry

Stores Docker images.

---

## AKS

Runs containers.

Benefits:

- Kubernetes orchestration
- Scalability

---

## Blob Storage

Stores:

- Models
- Reports
- Screenshots

---

# Security

- Managed Identity
- Key Vault
- NSG
- Private Endpoint

---

# Monitoring

Azure Monitor tracks:

- CPU
- Memory
- Requests
- API health

---

# Author

Mukaila Adesina

GitHub:

https://github.com/madesina2025

