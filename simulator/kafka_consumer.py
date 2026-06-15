from kafka import KafkaConsumer
import json
from sqlalchemy import create_engine
import pandas as pd

consumer = KafkaConsumer(
    "fraud_transactions",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("Listening for transactions...")

# engine = create_engine(
#     "postgresql://postgres:postgres@localhost:5432/fraud_detection"
    
# )

engine = create_engine("postgresql://fraud_user:fraud_password@localhost:5432/fraud_db")

for message in consumer:
    transaction = message.value

    amount = transaction["transaction_amount"]

    fraud_probability = 0.01

    if amount > 4000:
        fraud_probability = 0.95
    elif amount > 3000:
        fraud_probability = 0.80
    elif amount > 2000:
        fraud_probability = 0.60

    risk_label = "Fraud" if fraud_probability >= 0.70 else "Genuine"
    prediction = 1 if risk_label == "Fraud" else 0

    recommended_action = (
        "Flag for fraud review / possible block"
        if prediction == 1
        else "Approve transaction"
    )

    record = pd.DataFrame([{
        "customer_id": transaction["customer_id"],
        "merchant": transaction["merchant"],
        "country": transaction["country"],
        "channel": transaction["channel"],
        "transaction_amount": amount,
        "amount": amount,
        "prediction": prediction,
        "risk_label": risk_label,
        "fraud_probability": fraud_probability,
        "recommended_action": recommended_action
    }])

    record.to_sql(
        "fraud_predictions",
        engine,
        if_exists="append",
        index=False
    )

    print(
        transaction["customer_id"],
        amount,
        fraud_probability,
        risk_label,
        "Saved to PostgreSQL"
    )