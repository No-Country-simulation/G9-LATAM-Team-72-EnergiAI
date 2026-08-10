# EnergiAI — Frontend

Interfaz web del MVP de EnergiAI (Team 72 · Hackathon ONE G9 LATAM).
React 18 + Vite. Adaptada al **backend desplegado en Render**.

## Arrancar

```bash
npm install
npm run dev      # http://localhost:5173
```

El `.env` ya apunta al backend en Render. Para trabajar sin backend, deja
`VITE_API_URL` vacia y la app usa un simulador local.

## Backend (Render)

- API: `https://energiai-backend-g68o.onrender.com`
- Endpoint de analisis: `POST /api/analisis-energetico`
- Estado: `GET /api/`

Free tier: los servicios se duermen a los ~15 min y tardan 30-50 s en
despertar. La app hace un "warm-up" al cargar (GET /api/) y muestra un aviso
mientras el servicio despierta. El timeout de red es de 60 s por defecto
(`VITE_TIMEOUT_MS`).

## Contrato

`POST /api/analisis-energetico` — **camelCase**:

```json
{
  "consumoKwh": 420,
  "usoHorarioPico": true,
  "cantidadEquipos": 10,
  "tipoInmueble": "Casa",
  "horasAltoConsumo": 8
}
```

- `tipoInmueble`: `"Casa"` o `"Comercio"`.
- `superficieM2` (number, opcional): solo se envia cuando `tipoInmueble` es
  `"Comercio"`. Mejora la precision de la clasificacion en comercios.

Respuesta:

```json
{
  "categoria": "Ineficiente",
  "probabilidad": 0.77,
  "costoEstimadoMensual": 315.0,
  "recomendaciones": ["...", "...", "..."]
}
```

Errores de validacion: el backend responde 400 con un objeto `errors`
(campo -> mensaje); la UI los muestra juntos.

## Build y despliegue

```bash
npm run build     # /dist (estatico)
```

`base: './'`, sirve desde cualquier subcarpeta. Se puede desplegar como
Static Site en Render (mismo panel que ya usan) o en OCI Object Storage.
