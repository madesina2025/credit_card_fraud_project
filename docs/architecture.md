# Credit Card Fraud Detection System Architecture

```text
┌───────────────────────────────────────────────┐
│          Transaction Generator                │
│ (Simulated Credit Card Transactions)          │
└───────────────────┬───────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────────┐
│                FastAPI Service                │
│                                               │
│  • Receives transaction requests             │
│  • Performs validation                        │
│  • Calls ML prediction engine                 │
└───────────────────┬───────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────────┐
│          Fraud Detection Model                │
│                                               │
│  Random Forest Classifier                     │
│  Trained on Credit Card Fraud Dataset         │
└───────────────────┬───────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌─────────────────┐   ┌─────────────────────┐
│ Fraud Detected  │   │ Legitimate Payment  │
└────────┬────────┘   └──────────┬──────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
┌───────────────────────────────────────────────┐
│             PostgreSQL Database               │
│                                               │
│ Stores:                                       │
│ • Transaction Details                         │
│ • Prediction Scores                           │
│ • Fraud Flags                                 │
│ • Risk Levels                                 │
└───────────────────┬───────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────────┐
│                Dash Dashboard                 │
│                                               │
│ • Fraud Alerts                                │
│ • Fraud Trends                                │
│ • Risk Monitoring                             │
│ • Transaction Analysis                        │
│ • Executive KPIs                              │
└───────────────────────────────────────────────┘
```

## Future Real-Time Architecture

```text
┌───────────────┐
│ Live Payments │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Kafka Producer│
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Kafka Topic   │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│Kafka Consumer │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ FastAPI Fraud │
│ Prediction    │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ PostgreSQL    │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Dash Dashboard│
└───────────────┘
```