# ⚡ EnergiAI — Inteligencia para el Consumo Energético

> **Hackathon ONE G9 LATAM | Equipo 72**  
> *Plataforma de análisis inteligente, optimización y recomendación para el consumo energético en viviendas y comercios.*

---

## 📌 Visión del Proyecto

EnergiAI es una solución integral diseñada para transformar la manera en que los usuarios residenciales y comerciales monitorean, entienden y optimizan su consumo de energía eléctrica. Combinando modelos de Machine Learning, una arquitectura cloud escalable en Oracle Cloud Infrastructure (OCI) y una API robusta en Spring Boot, EnergiAI proporciona un diagnóstico preciso del perfil de eficiencia energética y ofrece recomendaciones accionables para reducir costos y huella de carbono.

---

## 🛠️ Arquitectura de la Solución

La plataforma se estructura en tres capas principales:

┌─────────────────────────────────────────┐
              │            Interfaz de Usuario          │
              │        (Frontend / Consumidor API)      │
              └────────────────────┬────────────────────┘
                                   │ POST /analisis-energetico
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           BACKEND & CLOUD                               │
│  ┌───────────────────────┐                  ┌────────────────────────┐  │
│  │ Spring Boot REST API  ├─────────────────►│ Modelo ML (.pkl/joblib)│  │
│  │ (Java 17)             │   Inferencia     │ Random Forest / XGBoost│  │
│  └───────────┬───────────┘                  └────────────────────────┘  │
│              │                                                          │
│              ▼                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ Oracle Cloud Infrastructure (OCI)                                │   │
│  │ Compute Instance | Virtual Cloud Network (VCN) | Security Rules  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘

1. **Data Science & ML:** Pipeline completo de Análisis Exploratorio de Datos (EDA), limpieza, tratamiento de variables y entrenamiento de modelos supervisados para clasificar el perfil de eficiencia (Eficiente, Moderado, Ineficiente).
2. **Backend API:** Servicio REST desarrollado en Java / Spring Boot que recibe la información del inmueble, consulta la inferencia del modelo y devuelve la categoría junto con su probabilidad.
3. **Infraestructura Cloud:** Despliegue seguro en OCI configurado con políticas de red (VCN, Ingress Rules) e instancias Compute optimizadas.

---

## 📊 Dataset & Pipeline de Datos

El repositorio incluye la estructura consolidada de los datos sintéticos/reales para el entrenamiento y benchmark del modelo:

* **Establecimientos:** Registro de consumos energéticos en sectores residenciales y comerciales analizados por el equipo para el modelo de ML.
* **Inventario de Equipos:** Consumos, potencias declaradas y penetración de tecnología Inverter.
* **Curva de Carga Horaria:** Distribución del consumo diario por franjas (Madrugada, Mañana, Tarde, Noche).
* **Consumo Mensual:** Facturación, costos en moneda local/USD e intensidad energética.

---

## 🚀 Integración del Servicio (API Backend)

El servicio REST desarrollado en Spring Boot expondrá un endpoint para el análisis energético:

* **Entrada (Request):** Datos del inmueble, consumo en kWh, inventario de equipos y patrones de uso horario.
* **Salida (Response):** Clasificación del nivel de eficiencia (`Eficiente`, `Moderado`, `Ineficiente`), probabilidad del modelo de ML y recomendaciones de optimización.

---

⚙️ Estructura del Repositorio

G9-LATAM-Team-72-EnergiAI/
├── data_Team_72_EnergiAI/               # Datasets, archivos CSV y curvas de carga
├── Benchmark_EnergiAI_Teams_72.xlsx      # Métricas de referencia y evaluación
├── Diccionario_datos_EnergiAI_Teams_72.xlsx # Definición de variables del modelo
├── Matriz_Logica_EnergiAI_Teams_72.xlsx  # Lógica de reglas de negocio
├── Project Hackaton ONE - G9 Team 72.pdf  # Brief y presentación oficial del proyecto
├── Team72_Energi_AI_Sprint_Planner.xlsx   # Planificador de Sprints y entregables
└── README.md                             # Documentación principal

---

## 👥 Integrantes del Equipo (Team 72)

* **Héctor Rafael Caraucán** — Project Manager 
* **Zuleyca Guadalupe Balles Soto** — Data Scientist
* **Luis Carlos Leguizamon Rojas** — Data Scientist
* **Alvaro Holguin Vega** — Backend Developer
* **Sandra Milena Arboleda Gomez** — Data Analyst
* **Arturo Morales** — Backend Developer
* **Lorena Bustos Castañeda** — Backend Developer

---

## 📄 Licencia

Este proyecto se desarrolla en el marco del Hackathon ONE G9 LATAM organizado por No Country, Oracle y Alura Latam.
