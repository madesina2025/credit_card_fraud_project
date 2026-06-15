from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from database.db import Base


class FraudPrediction(Base):
    __tablename__ = "fraud_predictions"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(String, nullable=True)
    merchant = Column(String, nullable=True)
    country = Column(String, nullable=True)
    channel = Column(String, nullable=True)
    transaction_amount = Column(Float, nullable=True)
    amount = Column(Float)
    prediction = Column(Integer)
    risk_label = Column(String)
    fraud_probability = Column(Float)
    recommended_action = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)