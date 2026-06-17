import pandas as pd
import joblib
import os

print("Loading test data...")

X_test = pd.read_csv("data/X_test.csv")
y_test = pd.read_csv("data/y_test.csv")

print("Loading model...")

model = joblib.load("models/random_forest_fraud_model.pkl")

print("Generating predictions...")

predictions = model.predict(X_test)

if hasattr(model, "predict_proba"):
    probabilities = model.predict_proba(X_test)[:, 1]
else:
    probabilities = [0] * len(predictions)

results = X_test.copy()

results["Actual_Class"] = y_test.iloc[:, 0]
results["Predicted_Class"] = predictions
results["Fraud_Probability"] = probabilities

if "Amount" not in results.columns:
    print("WARNING: Amount column not found")

os.makedirs("dashboard", exist_ok=True)

results.to_csv(
    "dashboard/flagged_transactions.csv",
    index=False
)

print("Dashboard file created successfully")
print(results.head())