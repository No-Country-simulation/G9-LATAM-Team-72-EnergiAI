# G9-LATAM-Team-72-EnergiAI
# Creación dataset para modelado - Equipo Data Science
# Versión 1.1

# ---------------------------------------------------------
# IMPORTAR LIBRERIAS
import pandas as pd
import numpy as np
import os

# ---------------------------------------------------------
# DEFINICIÓN DE RUTA
RUTA_DATA = r"E:\Estudios Vigentes\ESPECIALIZACION DATA SCIENCE ALURA ORACLE\Hackathon G9 Equipo 72\data_Team_72_EnergiAI"

# ---------------------------------------------------------
# CARGA / USO DE LOS DATAFRAMES SIMULADOS
df_est = pd.read_csv("establecimientos.csv")
df_eq = pd.read_csv("inventario_equipos.csv")
df_curv = pd.read_csv("curva_carga_horaria.csv")
df_cons = pd.read_csv("consumo_mensual.csv")

# ---------------------------------------------------------
# FEATURE ENGINEERING Y AGREGACIONES A NIVEL INMUEBLE
# Agregaciones de Inventario de Equipos (Tabla 2)
df_eq_agregado = df_eq.groupby('id_inmueble').apply(
    lambda g: pd.Series({
        'total_equipos': g['cantidad_equipos'].sum(),
        'potencia_total_watts': (g['potencia_watts'] * g['cantidad_equipos']).sum(),
        'tiene_inverter': 1 if g['tecnologia_inverter'].any() else 0,
        'porcentaje_inverter': round(g['tecnologia_inverter'].mean(), 4)
    })
).reset_index()

df_eq_agregado['porcentaje_inverter'] = df_eq_agregado['porcentaje_inverter'].round(4)

# Transformación de Curva Horaria a Columnas/Features (Tabla 3)
df_curva_pivot = df_curv.pivot(
    index='id_inmueble', 
    columns='franja_horaria', 
    values='porcentaje_distribucion'
).reset_index()

# Renombrar columnas pivotadas para mayor claridad
df_curva_pivot = df_curva_pivot.rename(columns={
    'Madrugada': 'pct_dist_madrugada',
    'Manana': 'pct_dist_manana',
    'Tarde': 'pct_dist_tarde',
    'Noche': 'pct_dist_noche'
})

# ---------------------------------------------------------
# MERGE Y CONSOLIDACIÓN RELACIONAL (JOINS)
# Consumo Mensual + Establecimientos
df_master = pd.merge(df_cons, df_est, on='id_inmueble', how='left')
# Equipos Agregados
df_master = pd.merge(df_master, df_eq_agregado, on='id_inmueble', how='left')
# Curva Horaria Pivotada
df_master = pd.merge(df_master, df_curva_pivot, on='id_inmueble', how='left')

# ---------------------------------------------------------
# VARIABLES DERIVADAS PARA EL MODELO DE IA
# Consumo diario promedio en kWh
df_master['consumo_kwh_dia'] = (df_master['consumo_kwh_mes'] / 30.0).round(4)

# Intensidad Energética (kWh/m2)
df_master['intensidad_energetica_kwh_m2'] = np.where(
    df_master['superficie_m2'] > 0,
    (df_master['consumo_kwh_mes'] / df_master['superficie_m2']).round(4),
    0.0
)

# Indicador de Franja Dominante de Consumo
franjas_cols = ['pct_dist_madrugada', 'pct_dist_manana', 'pct_dist_tarde', 'pct_dist_noche']
df_master['franja_pico_dominante'] = df_master[franjas_cols].idxmax(axis=1).str.replace('pct_dist_', '')

# Renombrar target para mantener consistencia
df_master = df_master.rename(columns={'perfil_calculado': 'efficiency_label'})

# ---------------------------------------------------------
# ORDENAMIENTO DE COLUMNAS Y EXPORTACIÓN
cols_ordenadas = [
    'id_registro', 'id_inmueble', 'anio_mes_dd', 'pais_ubicacion', 'tipo_establecimiento', 
    'categoria_comercio', 'superficie_m2', 'habitantes_empleados', 'total_equipos', 
    'potencia_total_watts', 'tiene_inverter', 'porcentaje_inverter', 'consumo_kwh_dia', 
    'consumo_kwh_mes', 'intensidad_energetica_kwh_m2', 'costo_factura_usd', 
    'costo_factura_moneda_local', 'codigo_moneda', 'pct_dist_madrugada', 
    'pct_dist_manana', 'pct_dist_tarde', 'pct_dist_noche', 'franja_pico_dominante', 
    'efficiency_label'
]

df_final = df_master[cols_ordenadas]

# Guardar en CSV
NOMBRE_SALIDA = 'dataset_team_72.csv'
df_final.to_csv(NOMBRE_SALIDA, index=False)

print(f"Archivo '{NOMBRE_SALIDA}' generado exitosamente.")
print(f"Dimensiones: {df_final.shape[0]} filas × {df_final.shape[1]} columnas.")
print("DISTRIBUCIÓN DEL TARGET (efficiency_label)")
print(df_final['efficiency_label'].value_counts())