# Dashboard Guide

## Real-Time Credit Card Fraud Detection Dashboard

## Overview

This dashboard provides real-time fraud monitoring and executive analytics for credit card transaction fraud detection.

It is built with:

- Dash
- Plotly
- Plotly Express
- Plotly Graph Objects
- SQLite

Dashboard URL:

http://127.0.0.1:8050

## Main Dashboard Sections

### Executive Dashboard

Shows the overall fraud position using:

- Total Transactions
- Live Fraud Alerts
- Genuine Transactions
- Live Fraud Exposure
- Fraud Rate
- Critical Alerts
- High Alerts
- Medium Alerts
- Low Alerts

### Fraud Operations Alert Panel

Displays the current fraud situation:

- Total Fraud Count
- Total Fraud Exposure
- Highest Risk Merchant
- Highest Risk Country
- Most Attacked Channel
- Live Fraud Rate

### KPI Cards

The KPI cards provide fast executive visibility:

- Live Fraud Alerts
- Live Genuine Transactions
- Live Fraud Exposure
- Fraud Rate
- Critical Alerts
- High Alerts
- Medium Alerts
- Low Alerts

### Live Fraud Risk Gauge

The gauge shows the current fraud rate as a percentage.

Risk interpretation:

- Low risk: low fraud rate
- Medium risk: moderate fraud rate
- High risk: high fraud rate
- Critical risk: severe fraud rate

### Fraud Heat Map by Hour

Shows fraud concentration by hour and minute.

Purpose:

- Identify fraud spikes
- Detect high-risk time periods
- Support fraud operations monitoring

### Latest Fraud Alerts

Shows recent fraudulent transactions.

Fields include:

- Merchant
- Country
- Amount
- Fraud Probability

### Fraud Trend Over Time

Shows fraud movement over time using a live area chart.

Purpose:

- Monitor fraud spikes
- Track transaction risk behaviour
- Identify abnormal fraud activity

### Fraud Exposure by Merchant

Shows total fraud exposure by merchant.

Example merchants:

- Amazon
- Apple
- Netflix
- Tesco
- Uber

### Fraud Exposure by Country

Shows fraud exposure by country.

Example countries:

- UK
- US
- NG
- DE
- FR

### Fraud Exposure by Channel

Shows fraud exposure by channel.

Channels include:

- POS
- ATM
- Online
- Mobile App

### Top 5 Risk Countries

Shows the five countries with the highest fraud exposure.

### Top 5 Merchants

Shows the five merchants with the highest fraud exposure.

### Fraud Probability Distribution

Shows the distribution of model fraud probability scores.

Purpose:

- Understand model confidence
- Identify concentration of high-risk predictions
- Compare fraud and genuine probability ranges

### Live Alert Feed

Shows a live feed of recent high-risk transactions.

### Hourly Fraud Summary Table

Summarises fraud activity by hour.

Typical fields:

- Hour
- Fraud Count
- Fraud Exposure
- Average Fraud Probability

### Top 10 Highest Risk Transactions

Displays the highest-risk transactions ranked by fraud probability.

Fields include:

- ID
- Customer
- Merchant
- Country
- Channel
- Amount
- Fraud Probability
- Risk Category
- Recommended Action
- Created At

## Risk Categories

| Risk Category | Condition |
|---|---|
| Critical | Fraud probability greater than or equal to 0.90 |
| High | Fraud probability from 0.70 to 0.89 |
| Medium | Fraud probability from 0.40 to 0.69 |
| Low | Fraud probability below 0.40 |

## Recommended Actions

| Risk Label | Recommended Action |
|---|---|
| Fraud | Flag for fraud review / possible block |
| Genuine | Approve transaction |

## Auto Refresh

The dashboard refreshes automatically every 5 seconds.

Data source:

SQLite database.

## Dashboard Workflow

SQLite Database
↓
Dash Callback Engine
↓
KPI Cards
↓
Charts
↓
Tables
↓
Executive Monitoring

## Business Value

The dashboard supports:

- Real-time fraud monitoring
- Fraud exposure analysis
- Merchant risk analysis
- Country risk analysis
- Channel risk analysis
- Executive reporting
- Fraud operations decision making

## Future Enhancements

- Kafka real-time streaming
- PostgreSQL database
- Redis caching
- WebSocket live push
- Email alerts
- SMS alerts
- Cloud deployment
- Prometheus and Grafana monitoring

## Author

Mukaila Adesina

Data Engineer | BI Developer | Machine Learning Enthusiast

GitHub: https://github.com/madesina2025
