import joblib
import numpy as np
from pytorch_tabnet.tab_model import TabNetRegressor

def load_model_and_scaler():
    model = TabNetRegressor()
    model.load_model("app/model_data/weather_tabnet_model.zip")
    scaler = joblib.load("app/model_data/scalers.pkl")
    return model, scaler

def predict_temperature(model, scaler, input_array):
    input_scaled = scaler.transform(input_array)
    prediction = model.predict(input_scaled)
    return prediction.flatten()