# -----------------------------------------------------------
# ENTRENAMIENTO MODELO
# Entrenamos y comparamos tres clasificadores supervisados de Scikit-Learn sobre el dataset conformado (consumo_energia_sintetico.csv):
# Regresión Logística, Árbol de Decisión y Random Forest. 
# El objetivo es predecir la categoría de eficiencia (Eficiente / Moderado / Ineficiente) 
# a partir de los campos del contrato del API.

# -----------------------------------------------------------
# 1. PREPARACION DATOS
# Separamos features y target, y armamos un preprocesamiento con ColumnTransformer: 
# estandarizado para las numéricas, one-hot para tipo_inmueble y passthrough para la booleana. 
# Partición 80/20 estratificada por clase.

import pandas as pd
import numpy as np
import joblib, json
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, 
    f1_score, 
    classification_report, 
    confusion_matrix, 
    ConfusionMatrixDisplay
)

datos = pd.read_csv("consumo_energia_sintetico.csv")

X = datos.drop(columns=["id_inmueble", "categoria"])
y = datos["categoria"]

num_cols = ["consumo_kwh", "cantidad_equipos", "horas_alto_consumo", "superficie_m2"]
cat_cols = ["tipo_inmueble"]
bin_cols = ["uso_horario_pico"]

preprocesador = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(drop="first"), cat_cols),
    ("bin", "passthrough", bin_cols),
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

print(f"Entrenamiento: {X_train.shape[0]:,} filas")
print(f"Prueba:        {X_test.shape[0]:,} filas")
print(f"Clases (train): {dict(y_train.value_counts())}")

# -----------------------------------------------------------
# 2. ENTRENAMIENTO Y COMPARACION DE LOS TRES MODELOS
# Evaluamos cada modelo con validación cruzada estratificada (5 folds) sobre el set de entrenamiento 
# luego medimos en el set de prueba.

modelos = {
    "Regresion Logistica": LogisticRegression(max_iter=1000),
    "Arbol de Decision":   DecisionTreeClassifier(max_depth=6, random_state=42),
    "Random Forest":       RandomForestClassifier(n_estimators=200, random_state=42),
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
resultados = []
entrenados = {}

for nombre, clf in modelos.items():
    pipe = Pipeline([("prep", preprocesador), ("clf", clf)])
    cv_acc = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="accuracy").mean()
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    resultados.append({
        "Modelo": nombre,
        "CV Accuracy": round(cv_acc*100, 1),
        "Test Accuracy": round(accuracy_score(y_test, y_pred)*100, 1),
        "F1 Macro": round(f1_score(y_test, y_pred, average="macro"), 3),
    })
    entrenados[nombre] = pipe

tabla = pd.DataFrame(resultados).sort_values("F1 Macro", ascending=False).reset_index(drop=True)

# IMPRESIÓN DE RESULTADOS EN CONSOLA / NOTEBOOK
print("\n" + "="*70)
print("COMPARATIVA DE MODELOS DE MACHINE LEARNING")
print("="*70)

try:
    display(tabla)
except NameError:
    print(tabla.to_string(index=False))

# Grafica comparativa
fig, ax = plt.subplots(figsize=(9, 4.5))
x = np.arange(len(tabla)); w = 0.35
ax.bar(x - w/2, tabla["CV Accuracy"],   w, label="CV Accuracy",   color="#4c72b0")
ax.bar(x + w/2, tabla["Test Accuracy"], w, label="Test Accuracy", color="#55a868")
ax.set_xticks(x); ax.set_xticklabels(tabla["Modelo"], rotation=15)
ax.set_ylabel("Accuracy (%)"); ax.set_ylim(0, 105)
ax.set_title("Comparacion de modelos")
for i, r in tabla.iterrows():
    ax.text(i - w/2, r["CV Accuracy"]+1,   f'{r["CV Accuracy"]:.0f}',   ha="center", fontsize=8)
    ax.text(i + w/2, r["Test Accuracy"]+1, f'{r["Test Accuracy"]:.0f}', ha="center", fontsize=8)
ax.legend(); plt.tight_layout(); plt.show()

"""**Lectura de resultados:
El Random Forest es el mejor (F1 macro 0.98 aprox). 
La Regresión Logística se queda muy por debajo (54% aprox): al ser un modelo lineal, 
no captura los cortes por tercil, lo que confirma que la relación entre consumo y categoría es de umbrales, no lineal.
El árbol y el bosque sí modelan esos cortes.**"""

# -----------------------------------------------------------
# 3. EVALUACION DEL MEJOR MODELO
# Reporte de clasificación y matriz de confusión del modelo ganador.
mejor_nombre = tabla.iloc[0]["Modelo"]
mejor_modelo = entrenados[mejor_nombre]
y_pred = mejor_modelo.predict(X_test)

print("\n" + "="*70)
print(f"MODELO SELECCIONADO: {mejor_nombre}")
print("="*70 + "\n")

# 2. Reporte de Clasificación en Consola
print(classification_report(y_test, y_pred, digits=3))

# 3. Definición del orden de las clases para la matriz
PERF_ORDER = ["Eficiente", "Moderado", "Ineficiente"]

# 4. Generación y renderizado de la Matriz de Confusión
fig, ax = plt.subplots(figsize=(5.5, 5))
cm = confusion_matrix(y_test, y_pred, labels=PERF_ORDER)

ConfusionMatrixDisplay(cm, display_labels=PERF_ORDER).plot(
    ax=ax, 
    cmap="Blues", 
    colorbar=False
)

ax.set_title(f"Matriz de confusión — {mejor_nombre}")
plt.tight_layout()
plt.show()

# -----------------------------------------------------------
# 4. IMPORTANCIA DE VARIABLES
# Qué features pesan más en la decisión del modelo.
rf = entrenados["Random Forest"]
ohe_names = list(rf.named_steps["prep"].named_transformers_["cat"].get_feature_names_out(cat_cols))
feat_names = num_cols + ohe_names + bin_cols
importancias = pd.Series(rf.named_steps["clf"].feature_importances_, index=feat_names).sort_values()

fig, ax = plt.subplots(figsize=(9, 4))
importancias.plot.barh(ax=ax, color="#4c72b0")
ax.set_title("Importancia de variables (Random Forest)")
ax.set_xlabel("Importancia relativa")
plt.tight_layout(); plt.show()

print((importancias.sort_values(ascending=False)*100).round(1).to_string())

"""**Hallazgo del análisis:
consumo_kwh concentra 75% aprox de la importancia, lo que es coherente con el hallazgo de leakage del EDA: 
el modelo reproduce la regla de negocio más que aprender un patrón nuevo. 
superficie_m2 aparece en segundo lugar (15% aprox), confirmando que es la variable que permite clasificar bien a los comercios. 
horas_alto_consumo y uso_horario_pico aportan poco (<1% combinado); se conservan porque son campos del contrato, 
pero su peso predictivo es marginal con esta data.**"""

# -----------------------------------------------------------
# 5. SERIALIZACION DEL MODELO
# Exportamos el pipeline completo del mejor modelo (preprocesamiento + clasificador) a `.pkl` con `joblib`. 
# Al guardar el pipeline entero, el equipo de Backend puede pasar los datos crudos del contrato del API 
# sin re-implementar el preprocesamiento.

MODELO_PATH = "modelo_energiai_team72.pkl"
joblib.dump(mejor_modelo, MODELO_PATH)
print(f"Modelo guardado: {MODELO_PATH}  ({mejor_nombre})")

# Metadatos para backend: esquema de entrada y clases de salida
meta = {
    "modelo": mejor_nombre,
    "features_entrada": {
        "consumo_kwh": "float (kWh/mes)",
        "uso_horario_pico": "bool",
        "cantidad_equipos": "int",
        "tipo_inmueble": "str ('Casa' | 'Comercio')",
        "horas_alto_consumo": "int (0-24)",
        "superficie_m2": "float (requerido para comercios)",
    },
    "clases_salida": PERF_ORDER,
    "test_accuracy": float(tabla.iloc[0]["Test Accuracy"]),
    "f1_macro": float(tabla.iloc[0]["F1 Macro"]),
}
with open("modelo_metadata.json", "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)
print("Metadatos guardados: modelo_metadata.json")

# Prueba de carga: simular una peticion como la que enviaria el API
modelo_cargado = joblib.load(MODELO_PATH)

ejemplo = pd.DataFrame([{
    "consumo_kwh": 420.0,
    "uso_horario_pico": True,
    "cantidad_equipos": 10,
    "tipo_inmueble": "Comercio",
    "horas_alto_consumo": 12,
    "superficie_m2": 50.0,
}])

pred = modelo_cargado.predict(ejemplo)[0]
proba = modelo_cargado.predict_proba(ejemplo)[0]
clases = modelo_cargado.classes_

print("Ejemplo de inferencia (como la haria el backend):")
print(f"  categoria predicha : {pred}")
print(f"  probabilidad       : {max(proba)*100:.1f}%")
print("  distribucion completa:")
for c, p in sorted(zip(clases, proba), key=lambda t: -t[1]):
    print(f"    {c:12s} {p*100:5.1f}%")

"""**
Cierre:
El pipeline entrenado queda serializado en modelo_energiai_team72.pkl, acompañado de modelo_metadata.json 
con el esquema de entrada y las clases de salida. Backend puede cargarlo con joblib.load() y 
llamar .predict() / .predict_proba() pasando los campos del contrato del API, 
obteniendo la categoría y la probabilidad que consume el endpoint POST /analisis-energetico.

Nota: 
la exactitud alta (98% aprox) refleja en buena parte la naturaleza determinística de la data sintética (el target se deriva del consumo por umbral). 
Es adecuada para el MVP; en producción con datos reales —donde el consumo varía por hábitos, clima y aislamiento— 
se espera un desempeño más moderado y con mayor valor predictivo real.
**"""