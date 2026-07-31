# -----------------------------------------------------------
# IMPORTAR LIBRERIAS
import json

class MotorRecomendaciones:
    def __init__(self, json_path="reglas_recomendaciones.json", tarifa_kwh=0.75):
        self.json_path = json_path
        self.tarifa_kwh = tarifa_kwh
        self.reglas = []
        self.cargar_reglas()

    def cargar_reglas(self):
        """Carga el archivo JSON de reglas configurado en el backend."""
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                self.reglas = json.load(f)
            print(f"[OK] {len(self.reglas)} reglas JSON cargadas correctamente en el motor.")
        except Exception as e:
            print(f"[ERROR] No se pudo leer el archivo de reglas JSON: {e}")

    def calcular_costo_estimado(self, consumo_kwh: float) -> float:
        """
        Calcula el costo estimado mensual con la tarifa de referencia ($0.75 / kWh).
        """
        return round(float(consumo_kwh) * self.tarifa_kwh, 2)

    def evaluar_usuario(self, datos_usuario: dict) -> list:
        """
        Evalúa los parámetros ingresados contra las reglas del JSON 
        y devuelve una lista simple de recomendaciones (strings).
        """
        if not self.reglas:
            return []

        # Sanitización y formateo seguro del contexto de entrada
        contexto = {
            "consumo_kwh": float(datos_usuario.get("consumo_kwh", 0.0)),
            "uso_horario_pico": bool(datos_usuario.get("uso_horario_pico", False)),
            "cantidad_equipos": max(int(datos_usuario.get("cantidad_equipos", 1)), 1),
            "tipo_inmueble": str(datos_usuario.get("tipo_inmueble", "Casa")),
            "horas_alto_consumo": int(datos_usuario.get("horas_alto_consumo", 0)),
            "superficie_m2": float(datos_usuario.get("superficie_m2", 0.0)),
            "perfil_calculado": str(datos_usuario.get("perfil_calculado", "Moderado"))
        }

        segmento_usr = contexto["tipo_inmueble"]
        perfil_usr = contexto["perfil_calculado"]
        recomendaciones_activadas = []

        for regla in self.reglas:
            # 1. Filtrar por segmento (Casa / Comercio)
            if regla.get("segmento") != segmento_usr:
                continue

            # 2. Validar perfil calculado ('Cualquiera' o coincidencia parcial)
            perfil_regla = str(regla.get("perfil_calculado", ""))
            aplica_perfil = (perfil_regla == "Cualquiera") or (perfil_usr and perfil_usr in perfil_regla)

            if not aplica_perfil:
                continue

            # 3. Evaluar la condición dinámica
            condicion_str = regla.get("condicion", "")
            try:
                if eval(condicion_str, {}, contexto):
                    texto_rec = regla["recomendacion"]
                    # Evitar duplicados en la lista de respuesta
                    if texto_rec not in recomendaciones_activadas:
                        recomendaciones_activadas.append(texto_rec)
            except Exception as e:
                print(f"[WARN] Error al evaluar la condición '{condicion_str}': {e}")

        return recomendaciones_activadas

# ===============================================================
# PRUEBA DE FUNCIONAMIENTO LOCAL (POST /analisis-energetico)

if __name__ == "__main__":
    motor = MotorRecomendaciones("reglas_recomendaciones.json")

    # 1. Entrada enviada en la solicitud POST
    solicitud_post = {
        "consumo_kwh": 420,
        "uso_horario_pico": True,
        "cantidad_equipos": 10,
        "tipo_inmueble": "Casa",
        "horas_alto_consumo": 8
    }

    # 2. Simulamos la predicción obtenida por el modelo ML (.pkl)
    categoria_predicha = "Ineficiente"
    probabilidad_predicha = 0.81

    # 3. Inyectamos la categoría predicha para evaluar el motor
    solicitud_post["perfil_calculado"] = categoria_predicha

    # 4. Generamos las recomendaciones y la estimación financiera
    lista_recomendaciones = motor.evaluar_usuario(solicitud_post)
    costo_mensual = motor.calcular_costo_estimado(solicitud_post["consumo_kwh"])

    # 5. Construcción de la respuesta JSON final
    respuesta_json = {
        "categoria": categoria_predicha,
        "probabilidad": probabilidad_predicha,
        "recomendaciones": lista_recomendaciones,
        "costo_estimado_mensual": costo_mensual
    }

    import json as json_lib
    print("\n" + "="*60)
    print("RESPUESTA COMPLETA DEL ENDPOINT (JSON):")
    print("="*60)
    print(json_lib.dumps(respuesta_json, indent=4, ensure_ascii=False))