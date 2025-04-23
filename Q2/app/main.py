from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from app.model import load_model_and_scaler, predict_temperature

app = FastAPI()
model, scaler = load_model_and_scaler()

class WeatherInput(BaseModel):
    humidity: float
    pressure: float
    wind_speed: float

@app.post("/predict")
def predict(data: WeatherInput):
    input_array = np.array([[data.humidity, data.pressure, data.wind_speed]])
    temp = predict_temperature(model, scaler, input_array)
    return {"predicted_temperature": round(temp[0], 2)}