from schemas import PredictionRequest, PredictionResponse

def predict(request: PredictionRequest) -> PredictionResponse:

    return PredictionResponse(
        categoria = "ineficiente",
        probabilidad = 0.0,
        recomendaciones=[
            "Apagar las luces cuando no se utilicen.",
            "Reducir el consumo en horario pico.",
            "Revisar los equipos de mayor consumo."
        ]
    )