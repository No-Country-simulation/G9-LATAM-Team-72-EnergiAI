# -----------------------------------------------------------
# IMPORTAR LIBRERIAS
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter

# Configuración de estilo
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
pd.set_option('display.max_columns', None)

# 1. CARGA DEL DATASET
RUTA_CARPETA = r"E:\Estudios Vigentes\ESPECIALIZACION DATA SCIENCE ALURA ORACLE\Hackathon G9 Equipo 72\Notebook_Simple"
RUTA_CSV = os.path.join(RUTA_CARPETA, "dataset_simple_team_72.csv")

print(f"Cargando archivo desde: {RUTA_CSV}")
df = pd.read_csv(RUTA_CSV)

pd.set_option("display.max_columns", 40)
pd.set_option("display.width", 160)
plt.rcParams.update({
    "figure.figsize": (9, 4.5),
    "axes.grid": True,
    "grid.alpha": 0.25,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 10,
})

# Paleta consistente para el perfil de eficiencia
PERF_COLORS = {"Eficiente": "#2e8b57", "Moderado": "#e0a800", "Ineficiente": "#c0392b"}
PERF_ORDER = ["Eficiente", "Moderado", "Ineficiente"]
print("Librerias cargadas.")

# -----------------------------------------------------------
# 1. CARGA DE DATOS
# Resolucion robusta de la ruta de datos
CANDIDATES = ["data_simple_Team_72_EnergiAI", "data/data_simple_Team_72_EnergiAI", ".", "data"]
DATA_DIR = next((c for c in CANDIDATES if os.path.exists(os.path.join(c, "dataset_simple_team_72.csv"))), None)
assert DATA_DIR is not None, "No encuentro los CSV. Coloca la carpeta data_simple_Team_72_EnergiAI junto al notebook."
print("Usando DATA_DIR =", os.path.abspath(DATA_DIR))

est = pd.read_csv(os.path.join(DATA_DIR, "establecimientos.csv"))
eq  = pd.read_csv(os.path.join(DATA_DIR, "inventario_equipos.csv"))
con = pd.read_csv(os.path.join(DATA_DIR, "consumo_mensual.csv"))
cur = pd.read_csv(os.path.join(DATA_DIR, "curva_carga_horaria.csv"))
ds  = pd.read_csv(os.path.join(DATA_DIR, "dataset_simple_team_72.csv"))

tablas = {"establecimientos": est, "inventario_equipos": eq,
          "consumo_mensual": con, "curva_carga_horaria": cur, "dataset (consolidado)": ds}
for n, df in tablas.items():
    print(f"{n:26s} {df.shape[0]:>6,} filas x {df.shape[1]:>2} columnas")

# -----------------------------------------------------------
# 2. PERFILADO DE VARIABLES
# Para cada tabla revisamos tipo de dato, valores nulos, cardinalidad y estadísticos básicos.
def perfilar(df, nombre):
    print("="*70)
    print(f"TABLA:{nombre}({df.shape[0]:,} filas x {df.shape[1]} columnas)")
    print("="*70)
    resumen = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "nulos": df.isna().sum(),
        "%_nulos": (df.isna().mean()*100).round(2),
        "unicos": df.nunique(),
        "ejemplo": [df[c].dropna().iloc[0] if df[c].notna().any() else None for c in df.columns],
    })
    try:
        display(resumen)  # Si estás en Jupyter Notebook
    except NameError:
        print(resumen)    # Si estás en un script de Python (.py) normal
        
    print("\n")
    return resumen

perfilar(est, "establecimientos")
perfilar(eq, "inventario_equipos")
perfilar(con, "consumo_mensual")
perfilar(cur, "curva_carga_horaria")
perfilar(ds, "dataset_simple_team_72 (consolidado)")

# Estadisticos descriptivos de las variables numericas clave
num_cols = ["superficie_m2","habitantes_empleados","total_equipos","potencia_total_watts",
            "porcentaje_inverter","consumo_kwh_dia","consumo_kwh_mes",
            "intensidad_energetica_kwh_m2","costo_factura_usd"]
stats_df = ds[[c for c in num_cols if c in ds.columns]].describe().T.round(2)
print(stats_df)

# -----------------------------------------------------------
# 3. CALIDAD E INTEGRIDAD DE LA DATA
#Verificamos nulos, llaves, integridad referencial y cardinalidad entre tablas
checks = []
for n, df in tablas.items():
    checks.append((f"Nulos en {n}", int(df.isna().sum().sum()), 0))
valid = set(est.id_inmueble)
for n, df in [("inventario_equipos",eq),("consumo_mensual",con),("curva_carga_horaria",cur),("dataset",ds)]:
    checks.append((f"FK huerfanas en {n}", len(set(df.id_inmueble)-valid), 0))
checks.append(("Inmuebles sin equipos", len(valid-set(eq.id_inmueble)), 0))
checks.append(("Inmuebles con != 4 franjas", int((cur.groupby('id_inmueble').size()!=4).sum()), 0))
checks.append(("Inmuebles con != 1 consumo", int((con.groupby('id_inmueble').size()!=1).sum()), 0))

res = pd.DataFrame(checks, columns=["verificacion","valor","esperado"])
res["estado"] = np.where(res.valor==res.esperado, "OK", "REVISAR")

# IMPRESIÓN FORZADA EN CONSOLA
print("\n" + "="*70)
print("REPORTE DE INTEGRIDAD Y CALIDAD DE DATOS")
print("="*70)
print(res.to_string(index=False))

# -----------------------------------------------------------
# 4. ANALISIS UNIVARIADO - ESTABLECIMIENTOS
# Composición de la cartera: tipo de inmueble, país y variables físicas. 
# En el dataset simple no hay subcategorías de comercio; el inmueble es solo Vivienda o Comercio.
fig, axes = plt.subplots(1, 2, figsize=(13, 4))
est.tipo_establecimiento.value_counts().plot.bar(ax=axes[0], color="#4c72b0")
axes[0].set_title("Tipo de establecimiento"); axes[0].tick_params(axis='x', rotation=0)
est.pais_ubicacion.value_counts().plot.bar(ax=axes[1], color="#4c72b0")
axes[1].set_title("Pais"); axes[1].tick_params(axis='x', rotation=30)
plt.tight_layout(); plt.show()

print("Proporcion Vivienda vs Comercio:")
print((est.tipo_establecimiento.value_counts(normalize=True)*100).round(1).to_string())

fig, axes = plt.subplots(1, 2, figsize=(13, 4))
axes[0].hist(est.superficie_m2, bins=40, color="#55a868", edgecolor="white")
axes[0].set_title("Distribucion de superficie_m2"); axes[0].set_xlabel("m2")
axes[1].hist(est.habitantes_empleados, bins=range(0,14), color="#55a868", edgecolor="white")
axes[1].set_title("Distribucion de habitantes / empleados"); axes[1].set_xlabel("personas")
plt.tight_layout(); plt.show()

# -----------------------------------------------------------
# 5. ANALISIS UNIVARIADO - INVENTARIO EQUIPOS
# Mezcla de equipos, potencia declarada y penetración de tecnología Inverter. 
fig, axes = plt.subplots(1, 2, figsize=(14, 4.5))
eq.tipo_equipo.value_counts().plot.barh(ax=axes[0], color="#c44e52")
axes[0].set_title("Equipos por tipo"); axes[0].invert_yaxis()
inv = eq.tecnologia_inverter.value_counts()
axes[1].bar(inv.index.astype(str), inv.values, color=["#2e8b57","#c0392b"])
axes[1].set_title("Tecnologia Inverter (True = eficiente)")
plt.tight_layout(); plt.show()
print("Penetracion Inverter global: {:.1f}% de los equipos".format(eq.tecnologia_inverter.mean()*100))

tab = eq.groupby("tipo_equipo").agg(
    potencia_mediana_w=("potencia_watts","median"),
    horas_uso_mediana=("horas_uso_estimadas_dia","median"),
    kwh_dia_medio=("consumo_kwh_dia_equipo","mean"),
    n=("id_equipo","size")).round(2).sort_values("kwh_dia_medio", ascending=False)

print("="*70)
print("RESUMEN TÉCNICO Y DE CONSUMO POR TIPO DE EQUIPO")
print("="*70)

# Intenta usar display() si estás en Jupyter, de lo contrario print() con to_string()
try:
    display(tab)
except NameError:
    print(tab.to_string())

# -----------------------------------------------------------
# 6. CONSUMO, COSTO Y PERFIL DE EFICIENCIA
# Distribución del consumo mensual y de la intensidad energética de los comercios
fig, axes = plt.subplots(1, 2, figsize=(13, 4))
axes[0].hist(ds.consumo_kwh_mes, bins=50, color="#4c72b0", edgecolor="white")
axes[0].set_title("Consumo mensual (kWh)"); axes[0].set_xlabel("kWh/mes")
com = ds[ds.tipo_establecimiento=="Comercio"]
axes[1].hist(com.intensidad_energetica_kwh_m2, bins=50, color="#8172b3", edgecolor="white")
axes[1].set_title("Intensidad energetica - solo comercios"); axes[1].set_xlabel("kWh/m2/mes")
plt.tight_layout(); plt.show()

# -----------------------------------------------------------
# 7. CURVA DE CARGA HORARIA
# Perfil promedio de consumo por franja. El dataset simple ya trae las franjas como columnas (pct_dist_*).
FR = {"pct_dist_madrugada":"Madrugada","pct_dist_manana":"Manana",
      "pct_dist_tarde":"Tarde","pct_dist_noche":"Noche"}
cols_fr = list(FR.keys())
seg = ds.tipo_establecimiento

fig, ax = plt.subplots(figsize=(10,4.5))
for s, g in ds.groupby("tipo_establecimiento"):
    ax.plot(list(FR.values()), g[cols_fr].mean().values, marker="o", label=s)
ax.set_title("Perfil de carga promedio por segmento")
ax.set_ylabel("fraccion del consumo diario")
ax.yaxis.set_major_formatter(PercentFormatter(1.0))
ax.legend(); plt.tight_layout(); plt.show()

# Revision de porcentajes negativos en la curva
neg = ds[(ds[cols_fr] < 0).any(axis=1)]
print("Inmuebles con alguna franja negativa:", len(neg))
if len(neg):
    print("Se corrigen en la seccion 11 (piso positivo + renormalizacion).")
    df_neg_muestra=(neg[["id_inmueble","tipo_establecimiento"]+cols_fr].head())
# Renderizado según entorno (Jupyter vs Python script/console)
    try:
        display(df_neg_muestra)
    except NameError:
        print(df_neg_muestra.to_string(index=False))

"""**Hallazgo del análisis (calidad):
Se detectan 5 inmuebles con una franja de distribución en valor negativo, 
algo físicamente imposible (una franja no puede ser un porcentaje negativo del consumo diario). 
Es un residuo del generador de la curva. 
Se corrige en la sección 11 acotando cada franja a un piso positivo y renormalizando a 1.0. 
Impacto bajo (5 de 5000).**"""

# -----------------------------------------------------------
# 8. VARIABLE OBJETIVO (EFFICIENCY_LABEL)
# Distribución del target global y por segmento.
fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
g = ds.efficiency_label.value_counts().reindex(PERF_ORDER)
axes[0].bar(PERF_ORDER, g.values, color=[PERF_COLORS[p] for p in PERF_ORDER])
axes[0].set_title("Target GLOBAL")
for i,v in enumerate(g.values): axes[0].text(i, v, f"{v}\n{v/len(ds)*100:.1f}%", ha="center", va="bottom")
for ax, seg_name in zip(axes[1:], ["Vivienda","Comercio"]):
    sub = ds[ds.tipo_establecimiento==seg_name].efficiency_label.value_counts().reindex(PERF_ORDER).fillna(0)
    ax.bar(PERF_ORDER, sub.values, color=[PERF_COLORS[p] for p in PERF_ORDER])
    ax.set_title(f"Target — {seg_name}"); tot=sub.sum()
    for i,v in enumerate(sub.values): ax.text(i, v, f"{int(v)}\n{v/tot*100:.1f}%", ha="center", va="bottom")
plt.tight_layout(); plt.show()
print(ds.efficiency_label.value_counts().to_string())

"""**Hallazgo del análisis (balance):
El target viene balanceado a 33/33/33, y no solo a nivel global: 
también dentro de cada segmento (Vivienda y Comercio). 
Esto se debe a que los umbrales del dataset simple se definieron por terciles de cada segmento. 
Es una condición ideal para entrenamiento: ninguna clase queda infrarrepresentada, no hace falta rebalancear.**"""

# -----------------------------------------------------------
# 9. RELACION ENTRE CONSUMO Y ETIQUETA (DATA LEAKAGE)
# El efficiency_label se calcula por umbral sobre `consumo_kwh_dia` (viviendas) e `intensidad_energetica` (comercios). 
# Ambas magnitudes derivan de `consumo_kwh`, que es feature.
ds2 = ds.copy()
ds2["label_code"] = ds2.efficiency_label.map({"Eficiente":0,"Moderado":1,"Ineficiente":2})
corr_cols = [c for c in ["consumo_kwh_dia","consumo_kwh_mes","intensidad_energetica_kwh_m2",
             "potencia_total_watts","porcentaje_inverter","costo_factura_usd",
             "superficie_m2","total_equipos","label_code"] if c in ds2.columns]
corr = ds2[corr_cols].corr()
fig, ax = plt.subplots(figsize=(8.5,7))
im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(corr_cols))); ax.set_xticklabels(corr_cols, rotation=45, ha="right")
ax.set_yticks(range(len(corr_cols))); ax.set_yticklabels(corr_cols)
for i in range(len(corr_cols)):
    for j in range(len(corr_cols)):
        ax.text(j, i, f"{corr.iloc[i,j]:.2f}", ha="center", va="center",
                color="white" if abs(corr.iloc[i,j])>0.5 else "black", fontsize=8)
fig.colorbar(im, fraction=0.046, pad=0.04)
ax.set_title("Correlacion de features vs target (label_code)")
plt.tight_layout(); plt.show()

# Una regla de umbral sobre una sola columna reproduce el label
viv = ds[ds.tipo_establecimiento=="Vivienda"]
q = viv.consumo_kwh_dia.quantile([1/3, 2/3]).values
lab = pd.cut(viv.consumo_kwh_dia, [-np.inf, q[0], q[1], np.inf],
             labels=["Eficiente","Moderado","Ineficiente"]).astype(str)
print(f"Regla de tercil sobre consumo_kwh_dia reproduce el label en viviendas: {(lab==viv.efficiency_label).mean()*100:.1f}%")

"""**Hallazgo del análisis (leakage):
El target es una función determinística por umbral de `consumo_kwh_dia` / `intensidad_energetica`, 
columnas que se derivan de `consumo_kwh` (una feature). 
Un modelo que incluya el consumo alcanzará una exactitud muy alta reproduciendo la regla, 
más que "aprendiendo" un patrón. Es inherente a la naturaleza sintética de la data (el consumo se generó por fórmula, 
sin la variabilidad real de hábitos, clima o aislamiento). 
Para el MVP es aceptable —el contrato del API entrega `consumo_kwh`—, 
pero conviene no sobreinterpretar el accuracy y reportarlo con esta salvedad.**"""

# -----------------------------------------------------------
# 10. SEÑAL DE VARIABLES INDEPENDIENTES
# Variables que no derivan del cálculo del target y sí podrían aportar señal propia: 
# penetración Inverter, mezcla de equipos, país.
fig, axes = plt.subplots(1, 2, figsize=(14, 4.5))
viv = ds[ds.tipo_establecimiento=="Vivienda"]
data_box = [viv[viv.efficiency_label==p].porcentaje_inverter.values for p in PERF_ORDER if (viv.efficiency_label==p).any()]
labels_box = [p for p in PERF_ORDER if (viv.efficiency_label==p).any()]
axes[0].boxplot(data_box)
axes[0].set_xticks(range(1, len(labels_box)+1)); axes[0].set_xticklabels(labels_box)
axes[0].set_title("Viviendas: % Inverter vs perfil"); axes[0].set_ylabel("porcentaje_inverter")
pico = ds.groupby(["tipo_establecimiento","franja_pico_dominante"]).size().unstack(fill_value=0)
pico.plot.bar(ax=axes[1]); axes[1].set_title("Franja pico dominante por tipo")
axes[1].tick_params(axis='x', rotation=0); axes[1].legend(title="franja", fontsize=8)
plt.tight_layout(); plt.show()

# -----------------------------------------------------------
# 11. LIMPIEZA Y TRATAMIENTO DE VARIABLES
# Conformamos el dataset al esquema del contrato del API (POST /`analisis-energetico`), 
# corregimos las curvas negativas y derivamos las dos variables que el contrato pide y no existen directamente en las tablas.
# Esquema del contrato: `consumo_kwh`, `uso_horario_pico`, `cantidad_equipos`, `tipo_inmueble`, `horas_alto_consumo` -> salida `categoria`.

# 11.1 Corrección de las curvas de carga con porcentaje negativo
cols_fr = ["pct_dist_madrugada","pct_dist_manana","pct_dist_tarde","pct_dist_noche"]
FLOOR = 0.02
piv = ds.set_index("id_inmueble")[cols_fr].copy()
mask_neg = (piv < 0).any(axis=1)
print("Inmuebles con franja negativa (ANTES):", int(mask_neg.sum()))

sub = piv.loc[mask_neg].clip(lower=FLOOR)
piv.loc[mask_neg] = sub.div(sub.sum(axis=1), axis=0).round(4)
print("Inmuebles con franja negativa (DESPUES):", int((piv < 0).any(axis=1).sum()))
print("Sumas fuera de [0.98,1.02]:", int((piv.sum(axis=1).sub(1).abs()>0.02).sum()))

# devolver las franjas corregidas al dataset
for c in cols_fr:
    ds[c] = ds["id_inmueble"].map(piv[c])
# recomputar franja pico por si algun maximo cambio
ds["franja_pico_dominante"] = (ds[cols_fr].idxmax(axis=1)
                               .str.replace("pct_dist_","", regex=False))

# 11.2 Derivación de las dos variables del contrato
# `uso_horario_pico` (bool): True si la franja de mayor consumo cae en la ventana pico (Tarde o Noche).
# `horas_alto_consumo` (int): horas del día con consumo por encima del reparto uniforme, leídas de la curva. Se cuentan las franjas por encima de 0.25 (uniforme) y se multiplican por 6 h (cada franja = 6 h del día). Es una medida directa de "horas del día con consumo alto", en rango 0–24.

# uso_horario_pico
ds["uso_horario_pico"] = ds["franja_pico_dominante"].isin(["tarde","noche"])

# horas_alto_consumo (franjas por encima del uniforme x 6h)
UNIFORME = 0.25
HORAS_FRANJA = 6
ds["horas_alto_consumo"] = ((ds[cols_fr] > UNIFORME).sum(axis=1) * HORAS_FRANJA).astype(int)

print("uso_horario_pico  -> True en {:.1f}% de los inmuebles".format(ds.uso_horario_pico.mean()*100))
print("horas_alto_consumo:")
print(ds.horas_alto_consumo.value_counts().sort_index().to_string())

# 11.3 Conformado al esquema del contrato y exportación
#Mapeo: `consumo_kwh <- consumo_kwh_mes`, `cantidad_equipos <- total_equipos`, `tipo_inmueble` con Vivienda -> 
# "Casa". Se conserva `consumo_kwh` (campo obligatorio del contrato) 
# y se incluye `superficie_m2` para el cálculo de eficiencia de comercios.

MAP_TIPO = {"Vivienda":"Casa","Comercio":"Comercio"}
model_df = pd.DataFrame({
    "id_inmueble":        ds.id_inmueble,
    "consumo_kwh":        ds.consumo_kwh_mes.round(2),
    "uso_horario_pico":   ds.uso_horario_pico.astype(bool),
    "cantidad_equipos":   ds.total_equipos.astype(int),
    "tipo_inmueble":      ds.tipo_establecimiento.map(MAP_TIPO),
    "horas_alto_consumo": ds.horas_alto_consumo.astype(int),
    "superficie_m2":      ds.superficie_m2.round(2),
    "categoria":          ds.efficiency_label,
})

print("Shape:", model_df.shape)
print("Nulos:", int(model_df.isna().sum().sum()))
print("tipo_inmueble:", dict(model_df.tipo_inmueble.value_counts()))
print("categoria    :", dict(model_df.categoria.value_counts()))

model_df.to_csv("consumo_energia_sintetico.csv", index=False)
print("\nGuardado: consumo_energia_sintetico.csv")
model_df.head()

# -----------------------------------------------------------
# 12. CONCLUSIONES Y ESTADO PARA LA FASE DE MODELADO

# Calidad de la data. El dataset simple es sólido: sin nulos, sin llaves duplicadas ni referencias huérfanas; 
# costos e intensidad energética recalculan de forma exacta. El target viene balanceado 33/33/33 por segmento, 
# sin subcategorías de comercio, alineado a los 5 campos del contrato del API.

#Hallazgos del análisis:
# Balance — target 33/33/33 por terciles, ideal para clasificación.
# Calidad — 5 curvas con franja negativa (corregidas en la sección 11).
# Leakage — el target es determinístico a partir de consumo_kwh; 
# el accuracy será alto por diseño de la data sintética. Aceptable para el MVP; se reporta con la salvedad.

# Entregable de limpieza:
# Se generó consumo_energia_sintetico.csv, conformado al esquema del contrato, 
# con las curvas corregidas y las dos variables (uso_horario_pico, horas_alto_consumo) ya derivadas. 
# El dataset queda listo para entrenamiento.
