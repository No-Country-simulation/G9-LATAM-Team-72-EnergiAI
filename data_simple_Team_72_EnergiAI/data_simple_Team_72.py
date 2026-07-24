# G9-LATAM-Team-72-EnergiAI
# Simulación de Datos - Equipo Data Science
# Propuesta de data sin categorias en comercios y con distribución de muestra 75% viviendas y 25% comercios
# Versión 1.0

# ---------------------------------------------------------
# IMPORTAR LIBRERIAS
import pandas as pd
import numpy as np
import random
from datetime import datetime

# ---------------------------------------------------------
# CONFIGURACION DE REPRODUCTIVIDAD, TEAM 72
np.random.seed(72)
random.seed(72)

# ---------------------------------------------------------
# PARAMETROS REGIONALES DE LATINOAMERICA
paises_config = {
    "Colombia": {"moneda": "COP", "tipo_cambio_usd": 4100.0},
    "Chile": {"moneda": "CLP", "tipo_cambio_usd": 920.0},
    "Mexico": {"moneda": "MXN", "tipo_cambio_usd": 18.50},
    "Argentina": {"moneda": "ARS", "tipo_cambio_usd": 950.0},
    "Peru": {"moneda": "PEN", "tipo_cambio_usd": 3.75},
    "Brasil": {"moneda": "BRL", "tipo_cambio_usd": 5.45} 
}
lista_paises = list(paises_config.keys())

# ---------------------------------------------------------
# CANTIDAD DE REGISTROS A SIMULAR
num_inmuebles = 5000
establecimientos_data = []

# Configuración de distribución: 75% Viviendas, 25% Comercios
tipos_inmueble = ["Vivienda", "Comercio"]
probabilidades_tipo = [0.75, 0.25]

# ---------------------------------------------------------
# CREAR TABLA ESTABLECIMIENTOS
for i in range(1, num_inmuebles + 1):
    # Selección ponderada según las probabilidades definidas (75/25)
    tipo = random.choices(tipos_inmueble, weights=probabilidades_tipo, k=1)[0]
    pais = random.choice(lista_paises)
    
    if tipo == "Vivienda":
        id_inmueble = f"VIV-{i:05d}"
        categoria = "No Aplica"
        # Se usa una distribución normal (campana de Gauss) con media de 90 m2 y desviación estándar de 25
        m2 = int(np.random.normal(90, 25))  # Promedio 90m2
        m2 = max(40, min(m2, 250))          # Límites lógicos
        habitantes_empleados = random.randint(1, 6)
    else: # Comercios
        id_inmueble = f"COM-{i:05d}"
        m2 = random.randint(30, 200)  # Rango general para espacios comerciales
        habitantes_empleados = random.randint(2, 12)  # Representa empleados

    # Guardar todos los inmuebles (Sin categoría de comercio)
    establecimientos_data.append([id_inmueble, tipo, m2, habitantes_empleados, pais])

df_establecimientos = pd.DataFrame(establecimientos_data, columns=[
    "id_inmueble", "tipo_establecimiento", "superficie_m2", "habitantes_empleados", "pais_ubicacion"
])

# ---------------------------------------------------------
# CREAR TABLA INVENTARIO_EQUIPOS
equipos_data = []
equipo_id_counter = 1

for idx, row in df_establecimientos.iterrows():
    # 1. ILUMINACION: Obligatorio para el 100% de los inmuebles
    cant_ilum = random.randint(10, 30) if row['tipo_establecimiento'] == "Vivienda" else random.randint(20, 60)
    equipos_data.append([f"EQ-{equipo_id_counter:05d}", row['id_inmueble'], "Iluminacion", cant_ilum, 15, True, round(random.uniform(6, 12), 2)])
    equipo_id_counter += 1
    
    if row['tipo_establecimiento'] == "Vivienda":
        # 2. REFRIGERACION: Nevera hogareña
        inv = random.choice([True, False])
        equipos_data.append([f"EQ-{equipo_id_counter:05d}", row['id_inmueble'], "Refrigeracion", 1, 350 if not inv else 180, inv, 24.0])
        equipo_id_counter += 1
        
        # 3. OTROS/FUERZA MOTRIZ: Lavadora/Plancha
        equipos_data.append([f"EQ-{equipo_id_counter:05d}", row['id_inmueble'], "Otros / Fuerza Motriz", 1, 1200, False, 1.5])
        equipo_id_counter += 1
        
    else: # Es un Comercio
        # Equipamiento estándar para comercio genérico
        # Climatización
        inv_ac = random.choice([True, False])
        equipos_data.append([f"EQ-{equipo_id_counter:05d}", row['id_inmueble'], "Climatizacion", random.randint(1, 3), 2200, inv_ac, 9.0])
        equipo_id_counter += 1

        # Computación / Sistemas
        equipos_data.append([f"EQ-{equipo_id_counter:05d}", row['id_inmueble'], "Computacion", max(2, row['habitantes_empleados']), 150, True, 8.0])
        equipo_id_counter += 1
        
        # Refrigeración Comercial (opcional para un 40% de los comercios)
        if random.random() < 0.40:
            equipos_data.append([f"EQ-{equipo_id_counter:05d}", row['id_inmueble'], "Refrigeracion", random.randint(1, 2), 750, False, 24.0])
            equipo_id_counter += 1

df_equipos = pd.DataFrame(equipos_data, columns=[
    "id_equipo", "id_inmueble", "tipo_equipo", "cantidad_equipos", "potencia_watts", "tecnologia_inverter", "horas_uso_estimadas_dia"
])

# Convertir watts hora a kilowatts hora (kWh) división *1000
df_equipos['consumo_kwh_dia_equipo'] = (
    df_equipos['cantidad_equipos'] * df_equipos['potencia_watts'] * df_equipos['horas_uso_estimadas_dia'] / 1000.0
).round(4)

# ---------------------------------------------------------
# CREAR TABLA CURVA_CARGA_HORARIA 
curva_data = []
curva_id_counter = 1

for idx, row in df_establecimientos.iterrows():
    if row['tipo_establecimiento'] == "Vivienda":
        # Ruido para perfil residencial (Pico en la Noche)
        p_mad = random.uniform(0.08, 0.16)
        p_man = random.uniform(0.12, 0.22)
        p_tar = random.uniform(0.18, 0.28)
    else:
        # Ruido para perfil comercial general (Pico diurno: Mañana y Tarde)
        p_mad = random.uniform(0.05, 0.12)
        p_man = random.uniform(0.35, 0.45)
        p_tar = random.uniform(0.35, 0.45)

    p_noc = 1.0 - (p_mad + p_man + p_tar)
    dist = [p_mad, p_man, p_tar, p_noc]
    # Normalización para garantizar que sumen exactamente 1.0
    dist = [round(x / sum(dist), 4) for x in dist]
            
    franjas = ["Madrugada", "Manana", "Tarde", "Noche"]
    for f, p in zip(franjas, dist):
        curva_data.append([f"C-{curva_id_counter:05d}", row['id_inmueble'], f, p])
        curva_id_counter += 1

df_curva = pd.DataFrame(curva_data, columns=["id_curva", "id_inmueble", "franja_horaria", "porcentaje_distribucion"])

# ---------------------------------------------------------
# CREAR TABLA CONSUMO_MENSUAL
consumo_data = []
reg_id_counter = 1
TARIFA_USD_REF = 0.75  # Tarifa estandarizada del proyecto ($0.75 USD)

consumo_diario_por_inmueble = df_equipos.groupby('id_inmueble')['consumo_kwh_dia_equipo'].sum().to_dict()

# Generar consumo mensual en base a la suma real de equipos
for idx, row in df_establecimientos.iterrows():
    id_inm = row['id_inmueble']
    pais = row['pais_ubicacion']
    config_pais = paises_config[pais]
    moneda_local = config_pais["moneda"]
    tipo_cambio = config_pais["tipo_cambio_usd"]

    # Consumo real proveniente de la suma de equipos
    kwh_dia = consumo_diario_por_inmueble.get(id_inm, 0.0)
    kwh_mes = round(kwh_dia * 30, 2)
    
    # Determinación del perfil basado en las reglas del negocio
    if row['tipo_establecimiento'] == "Vivienda":
        if kwh_dia < 9.21: perfil = "Eficiente"
        elif 9.21 <= kwh_dia <= 12.36: perfil = "Moderado"
        else: perfil = "Ineficiente"
    else:  # Comercio
        m2 = row['superficie_m2']
        ie = kwh_mes / m2 if m2 > 0 else 0  # Intensidad Energética kWh/m2
        
        # Umbrales generales para el segmento comercial
        if ie < 12.87: perfil = "Eficiente"
        elif 12.87 <= ie <= 22.76: perfil = "Moderado"
        else: perfil = "Ineficiente"
            
    # Estructuración Financiera, cálculo USD y moneda local
    costo_usd = round(kwh_mes * TARIFA_USD_REF, 2)
    costo_moneda_local = round(costo_usd * tipo_cambio, 2)
    
    consumo_data.append([
        f"REG-{reg_id_counter:05d}", id_inm, "2026-07-01", 
        kwh_mes, costo_usd, costo_moneda_local, moneda_local, perfil
    ])
    reg_id_counter += 1

df_consumo = pd.DataFrame(consumo_data, columns=[
    "id_registro", "id_inmueble", "anio_mes_dd", 
    "consumo_kwh_mes", "costo_factura_usd", "costo_factura_moneda_local", "codigo_moneda", "perfil_calculado"
])

# -------------------------------------------------------
# ALMACENAMIENTO Y EXPORTACIÓN A CSV
df_establecimientos.to_csv("establecimientos.csv", index=False)
df_equipos.to_csv("inventario_equipos.csv", index=False)
df_curva.to_csv("curva_carga_horaria.csv", index=False)
df_consumo.to_csv("consumo_mensual.csv", index=False)

print("Base de Datos generada con éxito")
print(f"Total de inmuebles simulados: {len(df_establecimientos)}")
print(f"Distribución de perfiles generados:\n{df_consumo['perfil_calculado'].value_counts()}")