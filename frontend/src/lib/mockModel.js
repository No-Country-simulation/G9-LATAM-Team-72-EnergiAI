/**
 * Simulador local del modelo de clasificacion.
 *
 * PARA QUE SIRVE: permite desarrollar, demostrar y probar el frontend completo
 * mientras el backend y el modelo real (Sprint 2) todavia no estan listos.
 * Cuando el API responda, este archivo deja de usarse: basta definir
 * VITE_API_URL en el .env. La UI no cambia.
 *
 * IMPORTANTE: esta NO es la logica oficial de negocio. Los criterios reales de
 * clasificacion los define el equipo de Data Analytics (tarea T5) y el modelo
 * entrenado (T9). Esta simulacion solo imita la forma y el rango de la respuesta.
 *
 * CALIBRACION: las constantes estan ajustadas para que el ejemplo canonico del
 * enunciado del proyecto se reproduzca tal cual:
 *   entrada { consumoKwh: 420, usoHorarioPico: true, cantidadEquipos: 10,
 *             tipoInmueble: "Casa", horasAltoConsumo: 8 }
 *   salida  -> categoria "Ineficiente", probabilidad 0.81, costo 315.00
 */

// Consumo mensual de referencia (kWh) para un inmueble con 5 equipos.
const BASE_POR_INMUEBLE = { Casa: 250, Establecimiento: 600 }
const EQUIPOS_REFERENCIA = 5
const AJUSTE_POR_EQUIPO = 0.06 // cada equipo extra justifica +6% de consumo
const PENALIZACION_PICO = 0.30
const PESO_HORAS_ALTAS = 0.60

// Umbrales de intensidad de consumo.
const UMBRAL_EFICIENTE = 0.9
const UMBRAL_MODERADO = 1.3

/** Calcula el indice de intensidad de consumo (1.0 = lo esperado). */
export function calcularIndice(p) {
  const base = BASE_POR_INMUEBLE[p.tipoInmueble] ?? BASE_POR_INMUEBLE.Casa
  const equipos = Math.max(Number(p.cantidadEquipos) || 1, 1)
  const baseAjustada = base * (1 + AJUSTE_POR_EQUIPO * (equipos - EQUIPOS_REFERENCIA))

  let indice = Number(p.consumoKwh) / Math.max(baseAjustada, 1)
  if (p.usoHorarioPico) indice += PENALIZACION_PICO
  indice += (Math.min(Number(p.horasAltoConsumo) || 0, 24) / 24) * PESO_HORAS_ALTAS

  return Math.max(indice, 0)
}

function clasificar(indice) {
  if (indice < UMBRAL_EFICIENTE) {
    return { categoria: 'Eficiente', clase: 'ok',
      probabilidad: 0.62 + (UMBRAL_EFICIENTE - indice) * 0.40 }
  }
  if (indice < UMBRAL_MODERADO) {
    const centro = (UMBRAL_EFICIENTE + UMBRAL_MODERADO) / 2
    return { categoria: 'Moderado', clase: 'mid',
      probabilidad: 0.60 + (0.2 - Math.abs(indice - centro)) * 0.50 }
  }
  return { categoria: 'Ineficiente', clase: 'bad',
    probabilidad: 0.62 + (indice - UMBRAL_MODERADO) * 0.38 }
}

/** Motor de recomendaciones basado en reglas (equivalente al de la tarea T11). */
export function generarRecomendaciones(p, categoria) {
  const recs = []

  if (p.usoHorarioPico) {
    recs.push('Reducir el uso de equipos durante los horarios pico.')
  }
  if (Number(p.horasAltoConsumo) >= 6) {
    recs.push('Distribuir las actividades de mayor consumo a lo largo del dia.')
  }
  if (categoria !== 'Eficiente') {
    recs.push('Evaluar los aparatos con mayor consumo energetico.')
  }
  if (Number(p.cantidadEquipos) >= 12) {
    recs.push('Desconectar los equipos que permanecen encendidos sin uso.')
  }
  if (categoria === 'Eficiente') {
    recs.push('Mantener los habitos actuales y dar seguimiento al consumo mensual.')
  }
  if (recs.length < 3) {
    recs.push('Dar seguimiento a los indicadores de eficiencia a lo largo del tiempo.')
  }

  return recs.slice(0, 4)
}

/** Devuelve la misma forma que `normalizarRespuesta` del cliente del API. */
export function simularAnalisis(payload, tarifa = 0.75) {
  const indice = calcularIndice(payload)
  const { categoria, clase, probabilidad } = clasificar(indice)

  return {
    id: null,
    categoria,
    clase,
    probabilidad: Math.min(0.97, Math.round(probabilidad * 100) / 100),
    costoEstimadoMensual: Math.round(Number(payload.consumoKwh) * tarifa * 100) / 100,
    costoCalculadoEnCliente: true,
    recomendaciones: generarRecomendaciones(payload, categoria),
    entrada: payload,
    fecha: new Date().toISOString(),
    origen: 'simulador',
  }
}
