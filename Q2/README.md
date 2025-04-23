Weather Prediction API using TabNet & FastAPI

## Setup
```bash
pip install -r requirements.txt
python app/train_tabnet.py  # Train and save model
uvicorn app.main:app --reload  # Run API locally
```

## Endpoint
`POST /predict`
```json
{
  "humidity": 45.0,
  "pressure": 1010.0,
  "wind_speed": 5.0
}
```

### Response
```json
{
  "predicted_temperature": 23.56
}
