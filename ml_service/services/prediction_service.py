import joblib
import json
import pandas as pd

from schemas.prediction import PredictionRequest, PredictionResponse
from services.recommendation_service import MotorRecomendaciones
from services.model_service import model

motor_recomendaciones = MotorRecomendaciones()

#funcion para obetener la predicion del ML
def predict(request: PredictionRequest) -> PredictionResponse:

    #crear DataFrame con los Datos recibidos en el endPoint
    datos = pd.DataFrame([{
        "consumo_kwh": request.consumoKwh,
        "uso_horario_pico": request.usoHorarioPico,
        "cantidad_equipos": request.cantidadEquipos,
        "tipo_inmueble": request.tipoInmueble,
        "horas_alto_consumo": request.horasAltoConsumo,
        "superficie_m2": request.superficieM2
    }])

    #obtener prediciones del ML
    prediccion = model.predict(datos)[0]
    probabilidades = model.predict_proba(datos)
    probabilidad = max(probabilidades[0])

    # Datos para el motor de recomendaciones
    datos_dict = datos.iloc[0].to_dict()
    #Inyectamos la categoría calculada para evaluar el motor
    datos_dict["perfil_calculado"] = prediccion
    #generar recomendaciones
    lista_recomendaciones = motor_recomendaciones.evaluar_usuario(datos_dict)

    #respuesta generada segun el Perfil Calculado
    return PredictionResponse(
        categoria=str(prediccion),
        probabilidad=float(probabilidad),
        recomendaciones= lista_recomendaciones
    )