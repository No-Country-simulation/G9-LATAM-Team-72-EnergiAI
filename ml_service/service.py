from schemas import PredictionRequest, PredictionResponse

def predict(request: PredictionRequest) -> PredictionResponse:

    return PredictionResponse(
        categoria = "ineficiente",
        probabilidad = 0.0,
        recomendaciones = "apagar la luz"
    )