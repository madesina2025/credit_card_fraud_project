from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from database.db import Base, engine, SessionLocal
from database.models import FraudPrediction


app = FastAPI(title="Credit Card Fraud Detection API")
Base.metadata.create_all(bind=engine)

model = joblib.load("models/random_forest_fraud_model.pkl")


class Transaction(BaseModel):
    Time: float
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    transaction_amount: float
    Amount: float
    customer_id: str
    merchant: str
    country: str
    channel: str


@app.get("/")
def home():
    return {"message": "Credit Card Fraud Detection API is running"}



@app.post("/predict")
def predict(transaction: Transaction):
    # input_df = pd.DataFrame([transaction.dict()])
    transaction_data = transaction.dict()

    model_features = transaction_data.copy()

    customer_id = model_features.pop("customer_id")
    merchant = model_features.pop("merchant")
    country = model_features.pop("country")
    channel = model_features.pop("channel")
    transaction_amount = model_features.pop("transaction_amount")
    input_df = pd.DataFrame([model_features])

    prediction = int(model.predict(input_df)[0])

    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(input_df)[0][1])
    else:
        probability = None

    if prediction == 1:
        action = "Flag for fraud review / possible block"
        risk_label = "Fraud"
    else:
        action = "Approve transaction"
        risk_label = "Genuine"

    db = SessionLocal()
    saved_prediction = FraudPrediction(
        customer_id=customer_id,
        merchant=merchant,
        country=country,
        channel=channel,
        transaction_amount=transaction.transaction_amount,
        amount=transaction.Amount,
        prediction=prediction,
        risk_label=risk_label,
        fraud_probability=probability,
        recommended_action=action
    )

    db.add(saved_prediction)
    db.commit()
    db.refresh(saved_prediction)
    db.close()

    return {
        "prediction": prediction,
        "risk_label": risk_label,
        "fraud_probability": probability,
        "recommended_action": action,
        "prediction_id": saved_prediction.id
    }

@app.get("/predictions")
def get_predictions():

    db = SessionLocal()

    predictions = db.query(FraudPrediction).all()

    results = []

    for row in predictions:
        results.append({
            "id": row.id,
            "amount": row.amount,
            "prediction": row.prediction,
            "risk_label": row.risk_label,
            "fraud_probability": row.fraud_probability,
            "recommended_action": row.recommended_action,
            "created_at": row.created_at
        })

    db.close()

    return results