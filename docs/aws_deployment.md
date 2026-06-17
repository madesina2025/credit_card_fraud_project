# AWS Deployment Guide

## Overview

The Credit Card Fraud Detection platform can be deployed entirely on AWS.

---

# Architecture

```text
Transaction Generator
        ↓
FastAPI API
        ↓
Random Forest Model
        ↓
PostgreSQL (RDS)
        ↓
Dash Dashboard
        ↓
CloudWatch Monitoring
```

---

# AWS Services

## EC2

Hosts:

- FastAPI
- Dash Dashboard

Purpose:

- Application server

---

## Amazon RDS PostgreSQL

Stores:

- Predictions
- Alerts
- Transactions

Benefits:

- Managed database
- High availability
- Automatic backups

---

## Amazon MSK (Kafka)

Future streaming platform.

Handles:

- Transaction ingestion
- Event processing

---

## CloudWatch

Monitors:

- CPU
- Memory
- Logs
- Network

---

## ECR

Stores Docker images.

Containers:

- FastAPI
- Dash

---

## ECS

Runs containers.

Benefits:

- Scalability
- High availability

---

## S3

Stores:

- Models
- Logs
- Reports
- Screenshots

---

# Deployment Flow

```text
FastAPI Container
        ↓
Random Forest Model
        ↓
RDS PostgreSQL
        ↓
Dash Dashboard
```

---

# Security

- IAM Roles
- Security Groups
- VPC
- Secrets Manager

---

# Monitoring

CloudWatch Metrics:

- API latency
- CPU utilization
- Memory usage
- Error rates

---

# Author

Mukaila Adesina

GitHub:

https://github.com/madesina2025

