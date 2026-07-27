from fastapi import FastAPI
from schemas import PredictionRequest
from service import predict

app = FastAPI(
    title="EnergiAI ML Service",
    description="Servicio de predicción del modelo de ML",
)

@app.get("/")
def home():
    return {
        "status": "OK",
        "message": "ML Service running"
    }

@app.post("/predict")
def prediction(request: PredictionRequest):
    return predict(request)

#iniciar la app
#uvicorn app:app --reload