# ☁️ Despliegue del Modelo en Oracle Cloud Infrastructure (OCI)

**Tarea T10:** Serializar el modelo (`pkl`/`joblib`) y subirlo a OCI Object Storage  
**Responsable:** Luis (Data Science)  
**Estado:** Finalizado  

---

## 📌 Resumen de Ejecución
Se almacenó de forma remota el artefacto binario del modelo entrenado (`Random Forest Pipeline`) en **OCI Object Storage** (Región: `mx-queretaro-1`) para permitir que la API del Backend consuma el modelo directamente vía HTTP.

---

## 🛠️ Detalles del Almacenamiento en OCI

* **Bucket:** `energiai-models`
* **Namespace:** `ax7imsqswlob`
* **Storage Tier:** Standard
* **Archivo:** `modelo_pkl-energiai_team72modelo_energiai_team72.pkl`
* **Tipo de Acceso:** Pre-Authenticated Request (PAR) de lectura para acceso del Backend.

### 🔗 Enlace PAR de Descarga Directa:
```text
[https://objectstorage.mx-queretaro-1.oraclecloud.com/p/uj2kUat0fjU1TcjE2QzFQed8d90Ok3tFQDEdg-M-E1h97Ce8YyC9Uv2dTx7idTru/n/ax7imsqswlob/b/energiai-models/o/modelo_pkl-energiai_team72modelo_energiai_team72.pkl](https://objectstorage.mx-queretaro-1.oraclecloud.com/p/uj2kUat0fjU1TcjE2QzFQed8d90Ok3tFQDEdg-M-E1h97Ce8YyC9Uv2dTx7idTru/n/ax7imsqswlob/b/energiai-models/o/modelo_pkl-energiai_team72modelo_energiai_team72.pkl)