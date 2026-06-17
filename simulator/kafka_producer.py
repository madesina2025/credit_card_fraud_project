from kafka import KafkaProducer
import json
import random
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

merchants = ["Amazon", "Apple", "Uber", "Tesco", "Netflix"]
countries = ["UK", "US", "FR", "DE", "NG"]
channels = ["Online", "POS", "ATM", "Mobile App"]

while True:

    transaction = {
    "customer_id": f"CUST{random.randint(1000, 9999)}",
    "merchant": random.choice(merchants),
    "country": random.choice(countries),
    "channel": random.choice(channels),

    # ML model features
    "amount": round(random.uniform(5, 5000), 2),
    "hour_of_day": random.randint(0, 23),
    "transactions_last_hour": random.randint(1, 30),
    "days_since_account_open": random.randint(1, 3000),
    "failed_login_attempts": random.randint(0, 7),
    "device_trust_score": round(random.uniform(0, 1), 4),
    }

    producer.send(
        "fraud_transactions_ml",
        transaction
    )
    producer.flush()

    print("Sent:", transaction)

    time.sleep(2)