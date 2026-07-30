# -----------------------------------------------------------
# IMPORTAR LIBRERIAS
import pandas as pd

# Datos sin acentos, tildes y caracteres especiales
datos_reglas = [
    {
        "segmento": "Viviendas",
        "perfil_calculado": "Cualquiera",
        "condicion": "franja_mayor_uso == 'Noche'",
        "diagnostico": "Concentración de demanda en la hora pico",
        "recomendacion": "Desplazamiento de Carga: Mueva los ciclos de mayor consumo fuera de la hora pico."
    },
    {
        "segmento": "Viviendas",
        "perfil_calculado": "Moderado / Ineficiente",
        "condicion": "porcentaje_distribucion_madrugada > 0.16",
        "diagnostico": "El consumo basal nocturno supera la línea base",
        "recomendacion": "Corte de Consumo Vampiro: Se detectó una fuga estática en la madrugada."
    },
    {
        "segmento": "Viviendas",
        "perfil_calculado": "Moderado / Ineficiente",
        "condicion": "tecnologia_inverter == False and tipo_equipo == 'Refrigeracion'",
        "diagnostico": "Presencia de un refrigerador de motor convencional",
        "recomendacion": "Sustitución Tecnológica Frigorífica: Su nevera consume más de lo óptimo."
    },
    {
        "segmento": "Viviendas",
        "perfil_calculado": "Ineficiente",
        "condicion": "horas_uso_estimadas_dia > 12.0 and tipo_equipo == 'Climatizacion'",
        "diagnostico": "Uso prolongado o a baja temperatura de aire acondicionado",
        "recomendacion": "Optimización de Climatización: Fije el aire acondicionado a 24°C."
    },
    {
        "segmento": "Comercio",
        "perfil_calculado": "Cualquiera",
        "condicion": "franja_mayor_uso == 'Mañana'",
        "diagnostico": "Alta simultaneidad de encendido en la apertura",
        "recomendacion": "Secuenciación de Encendido: Evite encender todos los equipos al mismo tiempo."
    },
    {
        "segmento": "Comercio",
        "perfil_calculado": "Moderado / Ineficiente",
        "condicion": "porcentaje_distribucion_noche > 0.15",
        "diagnostico": "Consumo residual elevado tras el cierre de operaciones",
        "recomendacion": "Protocolo de Cierre Eléctrico: Desarrolle una lista de chequeo de apagado nocturno."
    }
]

# Convertir a DataFrame y guardar con codificación UTF-8
df = pd.DataFrame(datos_reglas)
df.to_csv("reglas_recomendaciones.csv", index=False, encoding="utf-8-sig")

print("Archivo reglas_recomendaciones.csv creado con éxito")