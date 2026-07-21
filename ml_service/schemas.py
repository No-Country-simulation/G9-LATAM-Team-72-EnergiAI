from pydantic import BaseModel

class PredictionRequest(BaseModel):
    consumoKwh: float
    usoHorarioPico: bool
    cantidadEquipos: int
    tipoInmueble: str
    horasAltoConsumo: int

class PredictionResponse(BaseModel):
    categoria: str
    probabilidad: float
    recomendaciones: str