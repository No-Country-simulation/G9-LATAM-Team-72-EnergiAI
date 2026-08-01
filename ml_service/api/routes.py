from fastapi import APIRouter
from schemas.prediction import PredictionRequest
from schemas.prediction import PredictionResponse
from services.prediction_service import predict

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def prediction(request: PredictionRequest):
    return predict(request)