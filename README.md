# ⚡ EnergiAI — Inteligencia para el Consumo Energético

**Team 72 · Hackathon ONE G9 — LATAM**

## 🌱 ¿Qué es EnergiAI?

**EnergiAI** es una solución de análisis energético diseñada para ayudar a hogares y pequeños comercios a comprender mejor su consumo de electricidad.

La plataforma permite ingresar información básica sobre el consumo y las características del inmueble para generar un análisis energético mediante un servicio de Machine Learning.

El resultado proporciona:

* ⚡ Perfil energético actual.
* 📊 Probabilidad asociada a la clasificación.
* 💰 Impacto financiero estimado.
* 💡 Recomendaciones personalizadas.
* 📈 Historial y seguimiento de los análisis realizados.

La propuesta busca transformar información energética que puede resultar difícil de interpretar en resultados sencillos y accionables para el usuario.

---

# 🎯 Problema

El consumo de energía eléctrica representa un costo importante para hogares y pequeños comercios. Sin embargo, muchas personas conocen el valor de su factura, pero no necesariamente comprenden:

* qué tan eficiente es su consumo;
* qué factores pueden estar influyendo;
* cuánto representa económicamente su consumo;
* qué acciones podrían implementar para mejorarlo.

Las alternativas tradicionales de diagnóstico energético pueden requerir tiempo, conocimientos especializados y procesos que no siempre están al alcance de todos los usuarios.

**EnergiAI busca ofrecer una primera aproximación al diagnóstico energético de manera rápida, sencilla y comprensible.**

---

# 💡 Nuestra solución

EnergiAI utiliza una arquitectura de servicios que permite:

1. Recibir los datos proporcionados por el usuario.
2. Procesar la solicitud mediante un backend desarrollado con Spring Boot.
3. Consultar un servicio de Machine Learning desarrollado en Python.
4. Obtener una clasificación energética, una probabilidad y recomendaciones.
5. Presentar los resultados de manera visual y comprensible.
6. Registrar los análisis para facilitar su seguimiento.

---

# 🚀 MVP funcional

El MVP público de EnergiAI está disponible en:

**[Abrir EnergiAI — MVP funcional]**

[EnergiAI — MVP funcional](https://energiai-frontend-4x9w.onrender.com/)

> **Nota:** Los servicios están desplegados en Render. Dependiendo de su estado de disponibilidad, puede ser necesario esperar unos segundos para que los servicios estén disponibles antes de realizar una prueba.

---

# 🧩 Arquitectura de la solución

EnergiAI está compuesto por tres servicios principales:

```text
┌──────────────────────┐
│       USUARIO        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      FRONTEND        │
│   MVP / Render       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       BACKEND        │
│ Spring Boot / Java   │
└──────────┬───────────┘
           │
           │ /predict
           ▼
┌──────────────────────┐
│     ML SERVICE       │
│     Python / ML      │
└──────────┬───────────┘
           │
           │ categoría
           │ probabilidad
           │ recomendaciones
           ▼
┌──────────────────────┐
│       BACKEND        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      FRONTEND        │
│  Resultados /        │
│  Historial           │
└──────────────────────┘
```

## Servicios

### Frontend — MVP

Interfaz mediante la cual el usuario introduce los datos y consulta los resultados.

[Abrir Frontend / MVP](https://energiai-frontend-4x9w.onrender.com/)

### Backend API — Spring Boot / Java

Servicio encargado de la lógica de negocio, recepción de las solicitudes y coordinación de la comunicación con el servicio de Machine Learning.

[Abrir Backend API](https://energiai-backend-g68o.onrender.com/)

### ML Service — Python

Servicio encargado del análisis predictivo. El backend consulta este servicio para obtener la clasificación energética, la probabilidad y las recomendaciones correspondientes.

[Abrir ML Service](https://g9-latam-team-72-energiai.onrender.com/)

---

# 📝 Manual de usuario

## 1. Ingresar al MVP

Accede al MVP mediante:

[EnergiAI — MVP funcional](https://energiai-frontend-4x9w.onrender.com/)

La pantalla principal presenta la sección:

### Análisis de Consumo Eléctrico

Desde allí se pueden ingresar los datos necesarios para realizar un análisis.

---

## 2. Completar el formulario

Actualmente el MVP solicita **cinco datos principales**.

### 2.1 Consumo mensual

**Campo:** `Consumo mensual (kWh)`

Indica la cantidad de energía eléctrica consumida durante un mes.

La unidad utilizada es:

**kWh — kilovatios-hora.**

Ejemplo:

```text
420
```

---

### 2.2 Horarios de mayor utilización

**Campo:** `Horarios de mayor utilización`

Permite indicar si existe mayor utilización de energía durante determinados horarios.

Opciones:

* Sí
* No

---

### 2.3 Cantidad de equipos

**Campo:** `Cantidad de equipos`

Indica la cantidad de equipos eléctricos considerados para el análisis.

Ejemplo:

```text
10
```

---

### 2.4 Tipo de inmueble

**Campo:** `Tipo de inmueble`

Permite seleccionar el tipo de inmueble.

Opciones disponibles:

* Casa
* Comercio

---

### 2.5 Horas de alto consumo

**Campo:** `Horas de alto consumo`

Indica aproximadamente cuántas horas durante el día se presenta un mayor nivel de consumo.

Ejemplo:

```text
8
```

---

# 🔎 3. Ejecutar el análisis

Después de completar los cinco campos, selecciona:

## Analizar mi perfil

El sistema procesa la información y presenta el resultado correspondiente al escenario ingresado.

---

# 📊 4. Interpretar los resultados

## Perfil Energético Actual

El primer bloque presenta la clasificación energética obtenida.

El MVP contempla categorías como:

### 🟢 Eficiente

Representa un escenario con un comportamiento energético favorable de acuerdo con los criterios utilizados por el modelo.

### 🟡 Moderado

Representa un escenario intermedio en el que existen oportunidades de mejorar el uso de la energía.

### 🔴 Ineficiente

Representa un escenario con mayores oportunidades de mejora en el comportamiento energético.

La categoría **puede cambiar dependiendo de los datos ingresados**.

---

# 📈 5. Probabilidad

Junto a la categoría energética se muestra un porcentaje.

Por ejemplo:

```text
Eficiente
Probabilidad: 97%
```

o, dependiendo de los datos analizados:

```text
Ineficiente
Probabilidad: 77%
```

La probabilidad es un porcentaje **devuelto por el servicio de Machine Learning asociado a la clasificación obtenida**.

### Importante

No debe interpretarse automáticamente como:

* porcentaje de ahorro;
* porcentaje de consumo;
* porcentaje de dinero perdido;
* porcentaje de eficiencia.

El valor puede cambiar cuando se modifican los datos utilizados para realizar el análisis.

> La interpretación matemática exacta de este porcentaje depende de la implementación del modelo de Machine Learning y no se define únicamente a partir de la interfaz del MVP.

---

# 💰 6. Impacto Financiero Estimado

El MVP presenta una estimación mensual asociada al consumo analizado.

También muestra una:

**Tarifa de referencia: $0.75 por kWh**

Por ejemplo, para un consumo de:

```text
220 kWh
```

el MVP muestra:

```text
$165.00 mensual
```

El cálculo de referencia es:

```text
220 kWh × $0.75/kWh = $165.00
```

Para otro escenario:

```text
420 kWh × $0.75/kWh = $315.00
```

Por lo tanto, el resultado mostrado corresponde a una **estimación financiera calculada utilizando la tarifa de referencia configurada en el MVP**.

> Este valor no debe interpretarse necesariamente como el valor exacto de una factura eléctrica real, ya que las tarifas pueden variar según el usuario, proveedor, ubicación y condiciones del servicio.

---

# 💡 7. Recomendaciones Personalizadas

El MVP presenta una sección denominada:

## Recomendaciones Personalizadas

Las recomendaciones se reciben como parte del resultado del análisis y buscan orientar al usuario hacia posibles acciones de mejora.

Algunos ejemplos observados durante las pruebas son:

* Reducir el uso de equipos durante los horarios pico.
* Distribuir las actividades de mayor consumo a lo largo del día.
* Evaluar equipos con alto consumo energético.

### Importante

La cantidad y el contenido de las recomendaciones **pueden variar según el resultado del análisis**.

EnergiAI no está limitado a mostrar una cantidad fija de recomendaciones.

---

# 📚 8. Historial y Seguimiento

EnergiAI incorpora una sección de:

## Historial y Seguimiento

Esta funcionalidad permite conservar y consultar los análisis realizados durante la sesión.

El historial puede mostrar:

| Información | Descripción                                               |
| ----------- | --------------------------------------------------------- |
| Fecha       | Momento en que se realizó el análisis                     |
| Inmueble    | Tipo de inmueble analizado                                |
| Consumo     | Consumo mensual registrado                                |
| Equipos     | Cantidad de equipos                                       |
| PICO        | Información relacionada con horarios de mayor utilización |
| Perfil      | Clasificación energética                                  |
| Costo       | Impacto financiero estimado                               |

También se presenta una gráfica para facilitar la visualización de los resultados.

---

## Ejemplo de seguimiento

Si se realizan dos análisis:

```text
Análisis 1
Consumo: 220 kWh
Costo: $165.00

Análisis 2
Consumo: 420 kWh
Costo: $315.00
```

El historial puede presentar:

```text
2 análisis
Consumo promedio: 320 kWh
Costo acumulado: $480.00
```

Los valores son consistentes con:

```text
(220 + 420) / 2 = 320 kWh
```

y:

```text
$165 + $315 = $480
```

---

## Limpiar historial

El MVP también dispone de la opción:

**Limpiar historial**

Esta opción permite eliminar los registros almacenados en el historial de la sesión.

---

# 🔄 9. Comparar diferentes escenarios

Una de las posibilidades del MVP es realizar diferentes análisis modificando los datos de entrada.

Por ejemplo, el usuario puede cambiar:

* Consumo mensual.
* Horarios de mayor utilización.
* Cantidad de equipos.
* Tipo de inmueble.
* Horas de alto consumo.

Después puede volver a seleccionar:

**Analizar mi perfil**

El nuevo análisis puede generar:

* una categoría diferente;
* una probabilidad diferente;
* un impacto financiero diferente;
* recomendaciones diferentes.

Esto permite comparar diferentes escenarios de consumo.

---

# 🔧 10. Flujo técnico

De manera simplificada, el procesamiento funciona así:

### Paso 1 — Usuario

El usuario completa los datos del formulario.

### Paso 2 — Frontend

El MVP recibe los datos y realiza la solicitud al backend.

### Paso 3 — Backend

El backend desarrollado con Spring Boot recibe y procesa la solicitud.

### Paso 4 — Machine Learning

El backend consulta el servicio ML mediante la API correspondiente.

El servicio devuelve información relacionada con:

* categoría;
* probabilidad;
* recomendaciones.

### Paso 5 — Backend

El backend procesa la respuesta del servicio ML.

### Paso 6 — Frontend

El frontend presenta los resultados al usuario.

### Paso 7 — Historial

El análisis queda disponible para el seguimiento dentro del MVP.

---

# 🛡️ 11. Validaciones y manejo de errores

El backend incorpora validaciones para evitar que se procesen datos inválidos.

Entre las validaciones implementadas se encuentran:

* El consumo es obligatorio y debe ser mayor que cero.
* La cantidad de equipos es obligatoria y debe ser mayor que cero.
* El tipo de inmueble es obligatorio.
* Las horas de alto consumo no pueden ser negativas.
* La superficie, cuando forma parte de la solicitud técnica, no puede ser negativa.

El backend también incorpora manejo de errores para responder adecuadamente ante solicitudes inválidas o errores internos.

Por ejemplo:

* **HTTP 400 — Bad Request:** cuando los datos enviados no cumplen las validaciones.
* **HTTP 500 — Internal Server Error:** ante errores internos no controlados.

---

# 🌐 12. Comunicación y disponibilidad de servicios

EnergiAI utiliza servicios independientes desplegados en Render.

Debido a las características del entorno, algunos servicios pueden encontrarse temporalmente inactivos cuando no han recibido solicitudes durante un período determinado.

Por esta razón, durante una demostración se recomienda verificar previamente que los servicios requeridos estén disponibles.

> No se documenta en este README un endpoint específico para “despertar” los servicios porque el procedimiento exacto depende de la configuración actual del despliegue.

---

# 🛠️ 13. Tecnologías utilizadas

## Frontend

* Aplicación web para interacción con el usuario.
* Despliegue en Render.

## Backend

* Java
* Spring Boot
* Spring Web
* Spring Validation
* Spring Data / componentes asociados al proyecto
* OpenAPI / Swagger
* Maven

## Machine Learning

* Python
* API del modelo predictivo

## Infraestructura

* Render
* Arquitectura basada en servicios independientes.

---

# 📖 14. Documentación de la API

La API del backend cuenta con documentación mediante **OpenAPI / Swagger**, donde se describen los endpoints, solicitudes y respuestas disponibles.

La documentación técnica debe utilizar los nombres de propiedades que recibe la API, manteniendo la convención **camelCase** adoptada oficialmente por el equipo.

Ejemplos de propiedades utilizadas por el backend:

```text
consumoKwh
usoHorarioPico
cantidadEquipos
tipoInmueble
horasAltoConsumo
superficieM2
```

> `superficieM2` forma parte del modelo técnico del backend, pero actualmente no se presenta como campo visible en el formulario principal del MVP. Por esta razón no se incluye como requisito del usuario en el manual de uso.

---

# 🧪 15. Ejemplo de prueba

Un escenario de prueba puede utilizar:

| Campo                 |   Valor |
| --------------------- | ------: |
| Consumo mensual       | 420 kWh |
| Mayor utilización     |      Sí |
| Cantidad de equipos   |      10 |
| Tipo de inmueble      |    Casa |
| Horas de alto consumo |       8 |

El sistema procesa estos datos y puede devolver una clasificación energética, una probabilidad, un impacto financiero estimado y recomendaciones.

En uno de los escenarios probados:

```text
Perfil: Ineficiente
Probabilidad: 77%
Impacto financiero: $315.00 mensual
Tarifa de referencia: $0.75/kWh
```

> Los resultados dependen de los datos utilizados en cada análisis y pueden cambiar al modificar el escenario.

---

# ⚠️ 16. Consideraciones y limitaciones

EnergiAI es un **MVP desarrollado durante un hackathon**.

Su propósito es proporcionar una primera orientación sobre el comportamiento energético a partir de los datos suministrados por el usuario.

Los resultados:

* dependen de la información ingresada;
* dependen del modelo de Machine Learning;
* utilizan una tarifa de referencia para la estimación financiera;
* no sustituyen una auditoría energética profesional;
* no sustituyen el valor oficial de una factura de energía.

La plataforma continúa siendo susceptible de mejoras y evolución en futuras versiones.

---

# 🔮 17. Posibles líneas de evolución

Entre las posibilidades de evolución planteadas para EnergiAI se encuentran:

* Alertas y recomendaciones automatizadas.
* Integración con canales como WhatsApp.
* Conexión con medidores inteligentes.
* Seguimiento más avanzado del consumo.
* Evolución hacia soluciones para hogares y empresas.
* Escalabilidad hacia modelos de negocio B2B y residencial.

Estas funcionalidades representan posibilidades de evolución del proyecto y no deben interpretarse como funcionalidades necesariamente disponibles en la versión actual del MVP.

---

# 👥 18. Equipo

## Team 72 — EnergiAI

Proyecto desarrollado durante el **Hackathon ONE G9 — LATAM**.

**Integrantes:**

* Lorena Bustos Castañeda
* Sandra Milena Arboleda Gómez
* Zuleyca Guadalupe Balles Soto
* Alvaro Holguín Vega
* Arturo Morales
* Héctor Rafael Caraucán Dávila
* Luis Carlos Leguizamon Rojas

**Países representados:**

* Colombia
* México

---

# 🔗 19. Enlaces del proyecto

### MVP funcional

[EnergiAI — MVP](https://energiai-frontend-4x9w.onrender.com/)

### Backend API

[EnergiAI — Backend API](https://energiai-backend-g68o.onrender.com/)

### ML Service

[EnergiAI — ML Service](https://g9-latam-team-72-energiai.onrender.com/)

---

# 🏆 Hackathon ONE G9 — LATAM

**EnergiAI — Inteligencia para el Consumo Energético**

Una solución orientada a convertir datos de consumo energético en información comprensible, recomendaciones accionables y herramientas para el seguimiento del comportamiento energético.
