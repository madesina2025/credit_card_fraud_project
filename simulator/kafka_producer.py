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
        "customer_id": f"CUST{random.randint(1000,9999)}",
        "merchant": random.choice(merchants),
        "country": random.choice(countries),
        "channel": random.choice(channels),
        "transaction_amount": round(random.uniform(10,5000),2)
    }

    producer.send(
        "fraud_transactions",
        transaction
    )

    print("Sent:", transaction)

    time.sleep(2)