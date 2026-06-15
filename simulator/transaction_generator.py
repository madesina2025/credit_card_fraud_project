import time
import random
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/predict"
DATA_PATH = "dashboard/flagged_transactions.csv"

df = pd.read_csv(DATA_PATH)

feature_df = df.drop(columns=["Actual_Class", "Predicted_Class"])

print("Transaction simulator started...")

while True:
    # transaction = feature_df.sample(1).to_dict("records")[0]
    transaction = feature_df.sample(1).to_dict("records")[0]

    transaction["customer_id"] = f"CUST{random.randint(1000, 9999)}"
    transaction["merchant"] = random.choice(["Amazon", "Tesco", "Apple", "Netflix", "Uber", "Shell", "ASDA"])
    transaction["country"] = random.choice(["UK", "US", "NG", "FR", "DE"])
    transaction["channel"] = random.choice(["Online", "POS", "ATM", "Mobile App"])

    real_amount = round(random.uniform(5, 5000), 2)
    transaction["transaction_amount"] = real_amount
    response = requests.post(API_URL, json=transaction)

    if response.status_code == 200:
        result = response.json()
        print(
            f"Prediction ID: {result['prediction_id']} | "
            f"Risk: {result['risk_label']} | "
            f"Probability: {result['fraud_probability']} | "
            f"Action: {result['recommended_action']}"
        )
    else:
        print("API error:", response.text)

    time.sleep(random.randint(3, 7))