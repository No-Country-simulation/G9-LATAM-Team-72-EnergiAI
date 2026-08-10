import { ESCENARIOS } from '../lib/escenarios'

const CAMPOS_NUMERICOS = ['consumoKwh', 'cantidadEquipos', 'horasAltoConsumo', 'superficieM2']

export default function FormularioAnalisis({
  datos, errores, cargando, escenarioActivo, onCambio, onEscenario, onAnalizar,
}) {
  const esComercio = datos.tipoInmueble === 'Comercio'

  const set = (campo) => (e) => {
    const v = e.target.value
    if (campo === 'usoHorarioPico') return onCambio(campo, v === 'true')
    if (CAMPOS_NUMERICOS.includes(campo)) return onCambio(campo, v === '' ? '' : Number(v))
    return onCambio(campo, v)
  }

  return (
    <>
      <div className="section-head">
        <div>
          <h2>Analisis de Consumo Electrico</h2>
          <p className="tag" style={{ margin: 0 }}>
            Carga un escenario de ejemplo o captura tus propios datos.
          </p>
        </div>
        <div className="escenarios">
          {ESCENARIOS.map((esc) => (
            <button
              key={esc.id}
              type="button"
              className={`chip ${escenarioActivo === esc.id ? 'active' : ''}`}
              title={esc.descripcion}
              onClick={() => onEscenario(esc)}
            >
              {esc.nombre}
            </button>
          ))}
        </div>
      </div>

      <div className="form">
        <div className="field">
          <label htmlFor="consumo">
            Consumo mensual (kWh) <span className="hint">- consumoKwh</span>
          </label>
          <input
            id="consumo" type="number" min="1" step="1"
            className={errores.consumoKwh ? 'err' : ''}
            value={datos.consumoKwh}
            onChange={set('consumoKwh')}
          />
          <span className="fielderr">{errores.consumoKwh}</span>
        </div>

        <div className="field">
          <label htmlFor="pico">
            Horarios de mayor utilizacion <span className="hint">- usoHorarioPico</span>
          </label>
          <select id="pico" value={String(datos.usoHorarioPico)} onChange={set('usoHorarioPico')}>
            <option value="true">Si</option>
            <option value="false">No</option>
          </select>
          <span className="fielderr" />
        </div>

        <div className="field">
          <label htmlFor="equipos">
            Cantidad de equipos <span className="hint">- cantidadEquipos</span>
          </label>
          <input
            id="equipos" type="number" min="1" step="1"
            className={errores.cantidadEquipos ? 'err' : ''}
            value={datos.cantidadEquipos}
            onChange={set('cantidadEquipos')}
          />
          <span className="fielderr">{errores.cantidadEquipos}</span>
        </div>

        <div className="field">
          <label htmlFor="tipo">
            Tipo de inmueble <span className="hint">- tipoInmueble</span>
          </label>
          <select
            id="tipo"
            className={errores.tipoInmueble ? 'err' : ''}
            value={datos.tipoInmueble}
            onChange={set('tipoInmueble')}
          >
            <option value="Casa">Casa</option>
            <option value="Comercio">Comercio</option>
          </select>
          <span className="fielderr">{errores.tipoInmueble}</span>
        </div>

        <div className="field">
          <label htmlFor="horas">
            Horas de alto consumo <span className="hint">- horasAltoConsumo</span>
          </label>
          <input
            id="horas" type="number" min="0" max="24" step="1"
            className={errores.horasAltoConsumo ? 'err' : ''}
            value={datos.horasAltoConsumo}
            onChange={set('horasAltoConsumo')}
          />
          <span className="fielderr">{errores.horasAltoConsumo}</span>
        </div>

        {esComercio ? (
          <div className="field">
            <label htmlFor="superficie">
              Superficie (m2) <span className="hint">- superficieM2 · opcional</span>
            </label>
            <input
              id="superficie" type="number" min="1" step="1"
              placeholder="Mejora la precision en comercios"
              className={errores.superficieM2 ? 'err' : ''}
              value={datos.superficieM2}
              onChange={set('superficieM2')}
            />
            <span className="fielderr">{errores.superficieM2}</span>
          </div>
        ) : (
          <div className="field" />
        )}

        <button className="cta" onClick={onAnalizar} disabled={cargando}>
          {cargando && <span className="spinner" />}
          {cargando ? 'Analizando...' : 'Analizar mi perfil'}
        </button>
      </div>
    </>
  )
}
