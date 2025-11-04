# src/predict_helper.py
import joblib
import numpy as np

model = joblib.load('model/logistic_model.joblib')
scaler = joblib.load('model/scaler.joblib')

def predict_one(recency, frequency, monetary):
    x = scaler.transform([[recency, frequency, monetary]])
    prob = model.predict_proba(x)[0,1]
    pred = model.predict(x)[0]
    return pred, prob
