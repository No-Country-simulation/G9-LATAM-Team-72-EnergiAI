import pandas as pd

# Definir ruta archivos
RUTA_DATA = r"E:\Estudios Vigentes\ESPECIALIZACION DATA SCIENCE ALURA ORACLE\Hackathon G9 Equipo 72\data_Team_72_EnergiAI"

# Cargar las tablas generadas
df_establecimientos = pd.read_csv("establecimientos.csv")
df_consumo = pd.read_csv("consumo_mensual.csv")

# MERGE por la llave id_inmueble
df_establecimientos_consumo = pd.merge(
    df_establecimientos,
    df_consumo[["id_inmueble", "consumo_kwh_mes"]],
    on="id_inmueble"
)

# Calcular métricas derivadas para el cálculo de umbrales
# Consumo diario para viviendas
df_establecimientos_consumo["consumo_kwh_dia"] = (
    df_establecimientos_consumo["consumo_kwh_mes"] / 30.0
)

# Intensidad energética para comercios (kWh/m2 mensual)
df_establecimientos_consumo["intensidad_superficie"] = (
    df_establecimientos_consumo["consumo_kwh_mes"] / df_establecimientos_consumo["superficie_m2"]
)

# ---------------------------------------------------------
# CALCULO DE TERCILES AUTOMATICO (33.3% / 33.3% / 33.4%)
print("UMBRALES RECALCULADOS PARA VIVIENDA (kWh/día)")
viviendas = df_establecimientos_consumo[df_establecimientos_consumo["tipo_establecimiento"] == "Vivienda"]
t_viv = viviendas["consumo_kwh_dia"].quantile([0.333, 0.666]).values

print(f"Eficiente   : < {t_viv[0]:.2f} kWh/día")
print(f"Moderado    : {t_viv[0]:.2f} - {t_viv[1]:.2f} kWh/día")
print(f"Ineficiente : > {t_viv[1]:.2f} kWh/día")

print("UMBRALES RECALCULADOS PARA COMERCIO (kWh/m²·mes)")
comercios = df_establecimientos_consumo[df_establecimientos_consumo["tipo_establecimiento"] == "Comercio"]

# Mapeo descriptivo para imprimir con nombre completo
nombres_categorias = {
    "Categoria A": "Categoria A (Baja Intensidad: Oficinas, Papelerías, Tiendas)",
    "Categoria B": "Categoria B (Media-Alta Intensidad: Restaurantes, Cafeterías, Panaderías)",
    "Categoria C": "Categoria C (Alta Intensidad Continua: Abarrotes, Minimercados, Heladerías)"
}

for cat in sorted(comercios["categoria_comercio"].unique()):
    df_cat = comercios[comercios["categoria_comercio"] == cat]
    t_cat = df_cat["intensidad_superficie"].quantile([0.333, 0.666]).values

    print(f"Eficiente   : < {t_cat[0]:.2f} kWh/m²·mes")
    print(f"Moderado    : {t_cat[0]:.2f} - {t_cat[1]:.2f} kWh/m²·mes")
    print(f"Ineficiente : > {t_cat[1]:.2f} kWh/m²·mes")
