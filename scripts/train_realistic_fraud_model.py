import os
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


np.random.seed(42)

n_records = 20000

data = pd.DataFrame({
    "amount": np.random.uniform(5, 5000, n_records),
    "hour_of_day": np.random.randint(0, 24, n_records),
    "transactions_last_hour": np.random.randint(1, 30, n_records),
    "days_since_account_open": np.random.randint(1, 3000, n_records),
    "failed_login_attempts": np.random.randint(0, 8, n_records),
    "device_trust_score": np.random.uniform(0, 1, n_records),
})

data["is_fraud"] = (
    (
        (data["amount"] > 3000) &
        (data["device_trust_score"] < 0.35)
    )
    |
    (
        (data["transactions_last_hour"] > 15) &
        (data["failed_login_attempts"] >= 3)
    )
    |
    (
        (data["hour_of_day"].between(0, 5)) &
        (data["amount"] > 2000) &
        (data["device_trust_score"] < 0.50)
    )
    |
    (
        (data["days_since_account_open"] < 30) &
        (data["amount"] > 1500)
    )
).astype(int)

X = data.drop(columns=["is_fraud"])
y = data["is_fraud"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=10,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("Accuracy:", round(accuracy_score(y_test, y_pred), 4))
print("Precision:", round(precision_score(y_test, y_pred), 4))
print("Recall:", round(recall_score(y_test, y_pred), 4))
print("F1 Score:", round(f1_score(y_test, y_pred), 4))
print("ROC AUC:", round(roc_auc_score(y_test, y_prob), 4))

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/realistic_fraud_model.pkl")
joblib.dump(list(X.columns), "models/realistic_fraud_features.pkl")

print("Model saved to models/realistic_fraud_model.pkl")
print("Feature list saved to models/realistic_fraud_features.pkl")