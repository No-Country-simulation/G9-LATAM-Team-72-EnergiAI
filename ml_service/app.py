from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="EnergiAI ML Service",
    description="Servicio de predicción del modelo de ML",
)
#definir los endpoints
app.include_router(router)

#endpoint para verificar el funcionamiento de la API
@app.get("/")
def home():
    return {
        "status": "OK",
        "message": "ML Service running"
    }

#iniciar la app
#uvicorn app:app --reload