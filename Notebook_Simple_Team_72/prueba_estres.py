import asyncio
import time
import httpx

URL = "http://127.0.0.1:8000/analisis-energetico"
PAYLOAD = {
    "consumo_kwh": 420.0,
    "uso_horario_pico": True,
    "cantidad_equipos": 10,
    "tipo_inmueble": "Casa",
    "horas_alto_consumo": 8,
    "superficie_m2": 0.0
}

TOTAL_USUARIOS = 20
DURACION_SEGUNDOS = 60

peticiones_exitosas = 0
peticiones_fallidas = 0
tiempos_respuesta = []

async def simular_usuario(client, tiempo_fin):
    global peticiones_exitosas, peticiones_fallidas
    while time.time() < tiempo_fin:
        inicio = time.time()
        try:
            resp = await client.post(URL, json=PAYLOAD, timeout=5.0)
            latencia = (time.time() - inicio) * 1000
            if resp.status_code == 200:
                peticiones_exitosas += 1
                tiempos_respuesta.append(latencia)
            else:
                peticiones_fallidas += 1
        except Exception:
            peticiones_fallidas += 1
        await asyncio.sleep(0.1)

async def main():
    print(f"Iniciando prueba de carga: {TOTAL_USUARIOS} usuarios por {DURACION_SEGUNDOS} segundos...")
    tiempo_fin = time.time() + DURACION_SEGUNDOS
    
    async with httpx.AsyncClient() as client:
        tareas = [simular_usuario(client, tiempo_fin) for _ in range(TOTAL_USUARIOS)]
        await asyncio.gather(*tareas)
        
    print("\n" + "="*40)
    print("RESULTADOS DE LA PRUEBA DE ESTRÉS")
    print("="*40)
    print(f"Peticiones Exitosas: {peticiones_exitosas}")
    print(f"Peticiones Fallidas: {peticiones_fallidas}")
    if tiempos_respuesta:
        print(f"Tiempo Promedio de Respuesta: {sum(tiempos_respuesta)/len(tiempos_respuesta):.2f} ms")
        print(f"Tiempo Mínimo: {min(tiempos_respuesta):.2f} ms")
        print(f"Tiempo Máximo: {max(tiempos_respuesta):.2f} ms")

if __name__ == "__main__":
    asyncio.run(main())