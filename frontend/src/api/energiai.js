/**
 * Cliente del API de EnergiAI — adaptado al backend REAL desplegado en Render.
 *
 * Contrato vigente (el del backend desplegado, no el del brief):
 *
 *   POST {API_URL}/api/analisis-energetico
 *     body -> {
 *       consumoKwh:        number  (> 0)
 *       usoHorarioPico:    boolean
 *       cantidadEquipos:   number  (entero > 0)
 *       tipoInmueble:      "Casa" | "Comercio"
 *       horasAltoConsumo:  number  (entero >= 0)
 *       superficieM2?:     number  (opcional; se envia solo para Comercio)
 *     }
 *     res 200 -> { categoria, probabilidad, costoEstimadoMensual, recomendaciones[] }
 *     res 400 -> { timestamp, status, error, message, path, errors: {campo: msg} }
 *     res 503 -> ml_service no disponible
 *
 *   GET  {API_URL}/api/  -> estado del servicio (se usa para "despertar" el free tier)
 *
 * Nota Render free tier: los servicios se duermen a los ~15 min y tardan
 * 30-50 s en despertar. El primer POST puede tardar mucho; por eso hay un
 * "warm-up" opcional y timeouts largos.
 */

import { simularAnalisis } from '../lib/mockModel'

const RAW_URL = import.meta.env.VITE_API_URL ?? ''
export const API_URL = RAW_URL.replace(/\/$/, '')
export const USE_MOCK =
  import.meta.env.VITE_USE_MOCK === 'true' || API_URL === ''

export const TARIFA = Number(import.meta.env.VITE_TARIFA ?? 0.75)
export const MONEDA = import.meta.env.VITE_MONEDA ?? '$'

const RUTA_ANALISIS = '/api/analisis-energetico'
const RUTA_ESTADO = '/api/'

// Render puede tardar en frio; damos margen amplio.
const TIMEOUT_MS = Number(import.meta.env.VITE_TIMEOUT_MS ?? 60000)

/** fetch con AbortController para no colgarse indefinidamente. */
async function fetchConTimeout(url, opciones = {}, timeout = TIMEOUT_MS) {
  const ctrl = new AbortController()
  const id = setTimeout(() => ctrl.abort(), timeout)
  try {
    return await fetch(url, { ...opciones, signal: ctrl.signal })
  } finally {
    clearTimeout(id)
  }
}

/**
 * Construye el payload EXACTO que espera el backend (camelCase).
 * superficieM2 solo se incluye para Comercio y si trae valor.
 */
export function construirPayload(datos) {
  const payload = {
    consumoKwh: Number(datos.consumoKwh),
    usoHorarioPico: Boolean(datos.usoHorarioPico),
    cantidadEquipos: Number(datos.cantidadEquipos),
    tipoInmueble: String(datos.tipoInmueble),
    horasAltoConsumo: Number(datos.horasAltoConsumo),
  }
  if (
    datos.tipoInmueble === 'Comercio' &&
    datos.superficieM2 !== '' &&
    datos.superficieM2 != null &&
    Number.isFinite(Number(datos.superficieM2))
  ) {
    payload.superficieM2 = Number(datos.superficieM2)
  }
  return payload
}

/** Normaliza la categoria a Capitalizado para el color/etiqueta. */
export function normalizarCategoria(cat) {
  if (!cat) return 'Desconocido'
  const s = String(cat).trim()
  return s.charAt(0).toUpperCase() + s.slice(1).toLowerCase()
}

/** Clase de color: ok | mid | bad. */
export function claseCategoria(cat) {
  const c = String(cat || '').toLowerCase()
  if (c.startsWith('efic')) return 'ok'
  if (c.startsWith('mod')) return 'mid'
  return 'bad'
}

/** Aplana la respuesta del backend a la forma que consume la UI. */
export function normalizarRespuesta(data, payload) {
  const categoria = normalizarCategoria(data?.categoria)
  let probabilidad = Number(data?.probabilidad ?? 0)
  if (probabilidad > 1) probabilidad = probabilidad / 100

  let costo = data?.costoEstimadoMensual
  if (costo == null && payload) costo = payload.consumoKwh * TARIFA

  return {
    categoria,
    clase: claseCategoria(categoria),
    probabilidad,
    costoEstimadoMensual: Number(costo ?? 0),
    recomendaciones: Array.isArray(data?.recomendaciones) ? data.recomendaciones : [],
    entrada: payload,
    fecha: new Date().toISOString(),
    origen: 'api',
  }
}

/** Traduce un error del backend a un mensaje legible. */
async function leerError(res) {
  try {
    const err = await res.json()
    if (err.errors && typeof err.errors === 'object') {
      const detalles = Object.values(err.errors).join(' ')
      return detalles || err.message || `HTTP ${res.status}`
    }
    return err.message || err.error || `HTTP ${res.status}`
  } catch {
    if (res.status === 503) return 'El servicio de análisis no está disponible por el momento.'
    return `HTTP ${res.status}`
  }
}

/**
 * "Despierta" el backend de Render antes de la primera peticion real.
 * No lanza error si falla: es solo un intento de warm-up.
 */
export async function despertarServicio() {
  if (USE_MOCK) return true
  try {
    const res = await fetchConTimeout(`${API_URL}${RUTA_ESTADO}`, { method: 'GET' }, TIMEOUT_MS)
    return res.ok
  } catch {
    return false
  }
}

/** POST /api/analisis-energetico */
export async function analizarConsumo(datos) {
  const payload = construirPayload(datos)

  if (USE_MOCK) {
    await new Promise((r) => setTimeout(r, 450))
    return simularAnalisis(payload, TARIFA)
  }

  let res
  try {
    res = await fetchConTimeout(`${API_URL}${RUTA_ANALISIS}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
  } catch (e) {
    if (e.name === 'AbortError') {
      throw new Error('El servicio tardo demasiado en responder. Puede estar despertando; intenta de nuevo en un minuto.')
    }
    throw new Error('No se pudo contactar el servicio. Revisa tu conexion (o la configuracion de CORS del backend).')
  }

  if (!res.ok) throw new Error(await leerError(res))
  return normalizarRespuesta(await res.json(), payload)
}
