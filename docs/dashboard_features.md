# Dashboard Features

# Credit Card Fraud Detection Dashboard

---

# Overview

The dashboard provides real-time fraud monitoring and executive analytics.

Built using:

- Dash
- Plotly
- Plotly Express
- Plotly Graph Objects

Refresh Interval:

5 Seconds

Data Source:

SQLite Database

---

# Executive Dashboard

Provides a high-level summary of fraud activity.

Contains:

- Total Transactions
- Fraud Alerts
- Genuine Transactions
- Fraud Exposure
- Fraud Rate

---

# Fraud Operations Alert Panel

Purpose:

Provide operational awareness.

Displays:

- Total Fraud Exposure
- Highest Risk Merchant
- Highest Risk Country
- Most Attacked Channel
- Live Fraud Rate

---

# KPI Cards

Displays:

### Live Fraud Alerts

Number of fraudulent transactions.

---

### Live Genuine Transactions

Number of legitimate transactions.

---

### Fraud Exposure

Total monetary exposure.

---

### Fraud Rate

Fraud percentage.

---

### Critical Alerts

Transactions with probability ≥ 0.90

---

### High Alerts

Transactions with probability ≥ 0.70

---

### Medium Alerts

Transactions with probability ≥ 0.40

---

### Low Alerts

Transactions with probability < 0.40

---

# Risk Gauge

Type:

Speedometer Gauge

Purpose:

Measure current fraud risk.

Risk Zones:

- Green
- Yellow
- Orange
- Red

---

# Fraud Trend Over Time

Chart Type:

Area Chart

Purpose:

Monitor fraud activity over time.

Aggregation:

30-second intervals

Window:

Last 2 hours

---

# Fraud Heatmap by Hour

Chart Type:

Density Heatmap

Axes:

X-axis:

Minute

Y-axis:

Hour

Purpose:

Identify fraud spikes.

---

# Latest Fraud Alerts

Purpose:

Display recent suspicious transactions.

Fields:

- Merchant
- Country
- Channel
- Amount
- Fraud Probability

---

# Fraud Exposure by Merchant

Chart Type:

Bar Chart

Measures:

Total fraud exposure.

Examples:

- Amazon
- Netflix
- Apple
- Uber
- Tesco

---

# Fraud Exposure by Country

Chart Type:

Bar Chart

Examples:

- UK
- US
- NG
- DE
- FR

Purpose:

Geographical exposure analysis.

---

# Fraud Exposure by Channel

Chart Type:

Donut Chart

Channels:

- POS
- ATM
- Online
- Mobile App

Purpose:

Channel attack analysis.

---

# Top 5 Risk Countries

Chart Type:

Horizontal Bar Chart

Metric:

Fraud Exposure

Purpose:

Identify high-risk regions.

---

# Top 5 Merchants

Chart Type:

Horizontal Bar Chart

Metric:

Fraud Exposure

Purpose:

Identify vulnerable merchants.

---

# Fraud Probability Distribution

Chart Type:

Histogram

Purpose:

Visualize model confidence.

Colours:

Green:

Genuine

Red:

Fraud

---

# Live Fraud Alert Feed

Purpose:

Provide real-time visibility.

Contains:

- Merchant
- Country
- Channel
- Amount
- Fraud Probability

---

# Hourly Fraud Summary Table

Fields:

- Hour
- Fraud Count
- Fraud Exposure
- Average Fraud Probability

Purpose:

Operational reporting.

---

# Top 10 Highest Risk Transactions

Fields:

- Customer
- Merchant
- Country
- Channel
- Amount (£)
- Fraud Probability
- Risk Label
- Risk Category
- Recommended Action
- Timestamp

Purpose:

Prioritize investigations.

---

# Executive Summary Panel

Displays:

### Total Transactions

### Fraud Transactions

### Genuine Transactions

### Fraud Exposure

### Fraud Rate

### Average Fraud Probability

### Top Country

### Top Merchant

### Top Channel

---

# Dashboard Workflow

SQLite Database

↓

Dash Callback Engine

↓

Charts

↓

Tables

↓

KPIs

↓

Executive Analytics

↓

Fraud Monitoring

---

# Auto Refresh

Refresh Interval:

5 Seconds

Update Method:

Dash Interval Component

---

# Future Enhancements

## Streaming

Kafka

WebSockets

Redis

---

## Monitoring

Grafana

Prometheus

ELK Stack

---

## Alerts

Email Notifications

SMS Notifications

Microsoft Teams

Slack

---

## Cloud Deployment

AWS

Azure

GCP

---

# Business Value

Supports:

- Fraud Operations
- Risk Analytics
- Financial Crime Monitoring
- Executive Reporting
- Operational Intelligence

---

# Author

Mukaila Adesina

Data Engineer | BI Developer | Machine Learning Enthusiast

GitHub:

https://github.com/madesina2025

