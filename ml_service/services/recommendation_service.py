# -----------------------------------------------------------
# IMPORTAR LIBRERIAS
import json

class MotorRecomendaciones:
    def __init__(self, json_path="data/reglas_recomendaciones.json", tarifa_kwh=0.75):
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
        
       # Calcula el costo estimado mensual con la tarifa de referencia ($0.75 / kWh).
        
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