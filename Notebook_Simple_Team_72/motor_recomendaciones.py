# -----------------------------------------------------------
# IMPORTAR LIBRERIAS

import pandas as pd
import json

# -----------------------------------------------------------
# CARGUE DE REGLAS Y MOTOR DE RECOMENDACIONES
class MotorRecomendaciones:
    def __init__(self, csv_path="reglas_recomendaciones.csv"):
        self.csv_path = csv_path
        self.df_reglas = None
        self.cargar_reglas()

    def cargar_reglas(self):
        """Carga las reglas desde el archivo CSV."""
        try:
            self.df_reglas = pd.read_csv(self.csv_path)
            print(f"[OK] {len(self.df_reglas)} reglas cargadas correctamente desde CSV.")
        except Exception as e:
            print(f"[ERROR] No se pudo cargar el archivo CSV de reglas: {e}")

    def exportar_a_json(self, json_path="reglas_recomendaciones.json"):
        """Permite convertir el CSV a JSON para consumo directo en el backend."""
        if self.df_reglas is not None:
            reglas_dict = self.df_reglas.to_dict(orient="records")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(reglas_dict, f, indent=4, ensure_ascii=False)
            print(f"[OK] Reglas exportadas a JSON en: {json_path}")

    def evaluar_usuario(self, datos_usuario: dict) -> list:
        """
        Evalúa las variables del usuario contra las reglas cargadas.
        
        datos_usuario debe incluir:
          - segmento: 'Viviendas' o 'Comercio'
          - perfil_calculado: 'Eficiente', 'Moderado' o 'Ineficiente'
          - Demás indicadores (franja_mayor_uso, porcentaje_distribucion_madrugada, etc.)
        """
        if self.df_reglas is None:
            return []

        segmento_usr = datos_usuario.get("segmento")
        perfil_usr = datos_usuario.get("perfil_calculado")

        # 1. Filtrar por segmento (Viviendas o Comercio)
        reglas_segmento = self.df_reglas[self.df_reglas["segmento"] == segmento_usr]
        
        recomendaciones_activadas = []

        for _, regla in reglas_segmento.iterrows():
            perfil_regla = str(regla["perfil_calculado"])

            # 2. Validar coincidencia de perfil ("Cualquiera" o coincidencia parcial en "Moderado / Ineficiente")
            aplica_perfil = False
            if perfil_regla == "Cualquiera":
                aplica_perfil = True
            elif perfil_usr in perfil_regla:
                aplica_perfil = True

            if not aplica_perfil:
                continue

            # 3. Evaluar la condición técnica mediante eval()
            condicion_str = regla["condicion"]
            try:
                # eval() usa las claves de datos_usuario como variables locales
                if eval(condicion_str, {}, datos_usuario):
                    recomendaciones_activadas.append({
                        "diagnostico": regla["diagnostico"],
                        "recomendacion": regla["recomendacion"]
                    })
            except NameError:
                # Si a datos_usuario le falta alguna variable requerida por la regla, la ignora sin fallar
                pass
            except Exception as e:
                print(f"[WARN] Error al evaluar la condición '{condicion_str}': {e}")

        return recomendaciones_activadas

# -----------------------------------------------------------
# PRUEBA DE FUNCIONAMIENTO

if __name__ == "__main__":
    motor = MotorRecomendaciones("reglas_recomendaciones.csv")
    
    # Opcional: Generar el archivo JSON
    motor.exportar_a_json("reglas_recomendaciones.json")

    # Ejemplo de datos recibidos tras la clasificación del modelo
    inmueble_ejemplo = {
        "segmento": "Viviendas",
        "perfil_calculado": "Ineficiente",
        "franja_mayor_uso": "Noche",
        "porcentaje_distribucion_madrugada": 0.18,
        "tecnologia_inverter": False,
        "tipo_equipo": "Refrigeracion",
        "horas_uso_estimadas_dia": 14.0,
        "habitantes_empleados": 5,
        "cantidad_equipos": 4
    }

    print("\n" + "="*70)
    print("RECOMENDACIONES GENERADAS PARA EL INMUEBLE")
    print("="*70)
    
    res = motor.evaluar_usuario(inmueble_ejemplo)
    
    for i, r in enumerate(res, 1):
        print(f"\n[{i}] DIAGNÓSTICO : {r['diagnostico']}")
        print(f"    RECOMENDACIÓN: {r['recomendacion']}")