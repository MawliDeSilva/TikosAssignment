import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from pytorch_tabnet.tab_model import TabNetRegressor
import joblib

# Simulated weather data
humidity = np.random.uniform(30, 90, 500)
pressure = np.random.uniform(980, 1050, 500)
wind_speed = np.random.uniform(0, 15, 500)
temperature = 0.5 * humidity - 0.2 * pressure + 1.5 * wind_speed + np.random.normal(0, 3, 500)

X = np.stack([humidity, pressure, wind_speed], axis=1)
y = temperature.reshape(-1, 1)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)

model = TabNetRegressor()
model.fit(X_train=X_train, y_train=y_train, max_epochs=100)

model.save_model("app/model_data/weather_tabnet_model.zip")
joblib.dump(scaler, "app/model_data/scalers.pkl")