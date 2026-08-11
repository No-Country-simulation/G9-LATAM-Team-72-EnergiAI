/**
 * Ejemplos de utilizacion, cargables con un clic.
 *
 * IMPORTANTE: el backend acepta tipoInmueble = "Casa" | "Comercio".
 * Para "Comercio", la superficie (superficieM2) mejora la clasificacion y
 * es opcional en el contrato; se incluye en los escenarios de comercio.
 */
export const ESCENARIOS = [
  {
    id: 'eficiente',
    nombre: 'Casa eficiente',
    descripcion: 'Vivienda pequena, sin uso en horario pico',
    datos: {
      consumoKwh: 180,
      usoHorarioPico: false,
      cantidadEquipos: 6,
      tipoInmueble: 'Casa',
      horasAltoConsumo: 3,
      superficieM2: '',
    },
  },
  {
    id: 'enunciado',
    nombre: 'Caso del enunciado',
    descripcion: 'Ejemplo oficial del documento del proyecto',
    datos: {
      consumoKwh: 420,
      usoHorarioPico: true,
      cantidadEquipos: 10,
      tipoInmueble: 'Casa',
      horasAltoConsumo: 8,
      superficieM2: '',
    },
  },
  {
    id: 'comercio',
    nombre: 'Comercio',
    descripcion: 'Local comercial con superficie y consumo alto',
    datos: {
      consumoKwh: 700,
      usoHorarioPico: true,
      cantidadEquipos: 14,
      tipoInmueble: 'Comercio',
      horasAltoConsumo: 5,
      superficieM2: 120,
    },
  },
]

export const VALORES_INICIALES = {
  consumoKwh: 420,
  usoHorarioPico: true,
  cantidadEquipos: 10,
  tipoInmueble: 'Casa',
  horasAltoConsumo: 8,
  superficieM2: '',
}

/** Validaciones equivalentes a las del backend (@Positive, @PositiveOrZero, @NotBlank). */
export function validar(datos) {
  const errores = {}
  const consumo = Number(datos.consumoKwh)
  const equipos = Number(datos.cantidadEquipos)
  const horas = Number(datos.horasAltoConsumo)

  if (!Number.isFinite(consumo) || consumo <= 0) {
    errores.consumoKwh = 'Ingresa un consumo mayor a 0.'
  }
  if (!Number.isInteger(equipos) || equipos <= 0) {
    errores.cantidadEquipos = 'Ingresa un numero entero mayor a 0.'
  }
  if (!Number.isInteger(horas) || horas < 0 || horas > 24) {
    errores.horasAltoConsumo = 'Ingresa un valor entre 0 y 24.'
  }
  if (!datos.tipoInmueble) {
    errores.tipoInmueble = 'Selecciona el tipo de inmueble.'
  }
  // superficieM2 es opcional; si se captura, debe ser un numero positivo.
  if (datos.superficieM2 !== '' && datos.superficieM2 != null) {
    const sup = Number(datos.superficieM2)
    if (!Number.isFinite(sup) || sup <= 0) {
      errores.superficieM2 = 'Si la capturas, debe ser mayor a 0.'
    }
  }
  return errores
}
