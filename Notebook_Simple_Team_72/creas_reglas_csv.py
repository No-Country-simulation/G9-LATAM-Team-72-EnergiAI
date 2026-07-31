# -----------------------------------------------------------
# IMPORTAR LIBRERIAS
import pandas as pd
import json

def generar_archivos_reglas():
    # Matriz de reglas ajustada a la especificación real del API / ML:
    # Variables de entrada permitidas:
    # - consumo_kwh (float)
    # - uso_horario_pico (bool)
    # - cantidad_equipos (int)
    # - tipo_inmueble ('Casa' o 'Comercio')
    # - horas_alto_consumo (int)
    # - superficie_m2 (float)
    
    reglas_data = [
        # =============================================================
        # SEGMENTO: CASA
        {
            "segmento": "Casa",
            "perfil_calculado": "Cualquiera",
            "condicion": "uso_horario_pico == True",
            "diagnostico": "Concentración de demanda en la hora pico",
            "recomendacion": "Reducir el uso de equipos durante los horarios pico"
        },
        {
            "segmento": "Casa",
            "perfil_calculado": "Moderado / Ineficiente",
            "condicion": "(consumo_kwh / 30.0) > 12.36 and horas_alto_consumo > 6",
            "diagnostico": "El consumo basal nocturno supera la línea base",
            "recomendacion": "Distribuir las actividades de mayor consumo a lo largo del día"
        },
        {
            "segmento": "Casa",
            "perfil_calculado": "Moderado / Ineficiente",
            "condicion": "(consumo_kwh / cantidad_equipos) > 40.0",
            "diagnostico": "Presencia de electrodomésticos de alta intensidad de consumo",
            "recomendacion": "Evaluar equipos con alto consumo energético"
        },
        {
            "segmento": "Casa",
            "perfil_calculado": "Ineficiente",
            "condicion": "horas_alto_consumo > 10",
            "diagnostico": "Uso prolongado de sistemas de climatización o alto consumo",
            "recomendacion": "Optimizar el tiempo de uso continuo de electrodomésticos"
        },
        {
            "segmento": "Casa",
            "perfil_calculado": "Ineficiente",
            "condicion": "cantidad_equipos >= 3 and (consumo_kwh / 30.0) > 15.0",
            "diagnostico": "Consumo elevado por equipos térmicos o calentadores",
            "recomendacion": "Instalar temporizadores o ajustar la temperatura de calentadores"
        },

        # =============================================================
        # SEGMENTO: COMERCIO
        {
            "segmento": "Comercio",
            "perfil_calculado": "Moderado / Ineficiente",
            "condicion": "uso_horario_pico == False and horas_alto_consumo > 10",
            "diagnostico": "Alta simultaneidad de encendido en la apertura",
            "recomendacion": "Secuenciar el encendido de maquinaria y equipos en la apertura"
        },
        {
            "segmento": "Comercio",
            "perfil_calculado": "Moderado / Ineficiente",
            "condicion": "uso_horario_pico == True and horas_alto_consumo > 8",
            "diagnostico": "Consumo residual elevado tras el cierre de operaciones",
            "recomendacion": "Implementar un protocolo de cierre y apagado de cargas nocturnas"
        },
        {
            "segmento": "Comercio",
            "perfil_calculado": "Ineficiente",
            "condicion": "horas_alto_consumo > 12 and (consumo_kwh / cantidad_equipos) > 60.0",
            "diagnostico": "Uso de tecnologías de iluminación o equipos ineficientes",
            "recomendacion": "Modernizar la iluminación a tecnología LED y reemplazar equipos obsoletos"
        },
        {
            "segmento": "Comercio",
            "perfil_calculado": "Ineficiente",
            "condicion": "superficie_m2 > 0 and (consumo_kwh / superficie_m2) > 22.76",
            "diagnostico": "Alta densidad de consumo por metro cuadrado",
            "recomendacion": "Realizar auditoría térmica y mejorar el aislamiento del establecimiento"
        }
    ]

    # 1. Exportar a CSV para documentación en Excel
    df_reglas = pd.DataFrame(reglas_data)
    csv_path = "reglas_recomendaciones.csv"
    df_reglas.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"[OK] Archivo CSV creado exitosamente en: {csv_path}")

    # 2. Exportar a JSON para el Motor de Recomendaciones
    json_path = "reglas_recomendaciones.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(reglas_data, f, indent=4, ensure_ascii=False)
    print(f"[OK] Archivo JSON sincronizado creado exitosamente en: {json_path}")

if __name__ == "__main__":
    generar_archivos_reglas()