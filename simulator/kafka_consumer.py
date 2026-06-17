import sys
import os

import joblib
import pandas as pd

model = joblib.load("models/realistic_fraud_model.pkl")
model_features = joblib.load("models/realistic_fraud_features.pkl")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kafka import KafkaConsumer
import json
# from sqlalchemy import create_engine
# import pandas as pd

from database.db import SessionLocal
from database.models import FraudPrediction


consumer = KafkaConsumer(
    "fraud_transactions_ml",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id="fraud-dashboard-live-consumer-v2",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("Listening for transactions...")

# engine = create_engine(
#     "postgresql://postgres:postgres@localhost:5432/fraud_detection"
    
# )

# engine = create_engine("postgresql://fraud_user:fraud_password@localhost:5432/fraud_db")

for message in consumer:
    transaction = message.value

    if "amount" not in transaction:
        print("Skipping old transaction format:", transaction)
        continue

    amount = transaction["amount"]

    features = pd.DataFrame([{
        "amount": transaction["amount"],
        "hour_of_day": transaction["hour_of_day"],
        "transactions_last_hour": transaction["transactions_last_hour"],
        "days_since_account_open": transaction["days_since_account_open"],
        "failed_login_attempts": transaction["failed_login_attempts"],
        "device_trust_score": transaction["device_trust_score"],
    }])

    features = features[model_features]

    fraud_probability = float(model.predict_proba(features)[0][1])

    risk_label = "Fraud" if fraud_probability >= 0.50 else "Genuine"
    prediction = 1 if risk_label == "Fraud" else 0

    
    recommended_action = (
        "Flag for fraud review / possible block"
        if prediction == 1
        else "Approve transaction"
    )
    db = SessionLocal()

    record = FraudPrediction(
        customer_id=transaction["customer_id"],
        merchant=transaction["merchant"],
        country=transaction["country"],
        channel=transaction["channel"],
        transaction_amount=amount,
        prediction=prediction,
        risk_label=risk_label,
        fraud_probability=fraud_probability,
        recommended_action=recommended_action
    )

    db.add(record)
    db.commit()
    db.close()
   

    print(
        transaction["customer_id"],
        amount,
        fraud_probability,
        risk_label,
        "Saved to PostgreSQL"
    )