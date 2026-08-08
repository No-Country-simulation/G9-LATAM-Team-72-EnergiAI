from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from motor_recomendaciones import MotorRecomendaciones

app = FastAPI(
    title="API de Análisis Energético y Motor de Recomendaciones",
    version="1.0.0"
)

# Inicializar la clase del motor
motor = MotorRecomendaciones("reglas_recomendaciones.json")

# 1. Definir la estructura del JSON que enviará Postman
class SolicitudAnalisis(BaseModel):
    consumo_kwh: float
    uso_horario_pico: bool
    cantidad_equipos: int
    tipo_inmueble: str
    horas_alto_consumo: int
    superficie_m2: Optional[float] = 0.0
    perfil_calculado: Optional[str] = None


# 2. Función auxiliar para clasificar el perfil si no viene precalculado
def clasificar_perfil_automatico(consumo_kwh: float) -> tuple[str, float]:
    if consumo_kwh >= 300.0:
        return "Ineficiente", 0.81
    elif consumo_kwh >= 150.0:
        return "Moderado", 0.75
    else:
        return "Eficiente", 0.94


# 3. Endpoint principal POST /analisis-energetico
@app.post("/analisis-energetico")
def analizar_energia(datos: SolicitudAnalisis):
    try:
        # Convertir la entrada enviada por Postman a diccionario de Python
        datos_dict = datos.model_dump()

        # Determinar categoría y probabilidad si no fueron enviadas explícitamente
        if not datos_dict.get("perfil_calculado"):
            categoria, probabilidad = clasificar_perfil_automatico(datos_dict["consumo_kwh"])
            datos_dict["perfil_calculado"] = categoria
        else:
            categoria = datos_dict["perfil_calculado"]
            probabilidad = 0.85

        # Ejecuta los métodos exactos de MotorRecomendaciones
        lista_recomendaciones = motor.evaluar_usuario(datos_dict)
        costo_mensual = motor.calcular_costo_estimado(datos_dict["consumo_kwh"])

        # Retorna el JSON con la estructura solicitada
        return {
            "categoria": categoria,
            "probabilidad": probabilidad,
            "recomendaciones": lista_recomendaciones,
            "costo_estimado_mensual": costo_mensual
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el motor: {str(e)}")