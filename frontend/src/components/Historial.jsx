/**
 * Historial de analisis + grafico de seguimiento.
 *
 * Cubre los recursos opcionales del proyecto: historial de analisis,
 * visualizaciones graficas y comparacion entre periodos.
 *
 * Fuente de datos: el endpoint de consulta de resultados del API cuando esta
 * disponible; si no, los analisis hechos en esta sesion.
 */

const COLOR_CLASE = { ok: 'var(--ok)', mid: 'var(--mid)', bad: 'var(--bad)' }

function valorEntrada(item, clave, fallback = '-') {
  const entrada = item?.entrada ?? {}
  return entrada[clave] ?? entrada[clave.replace(/_([a-z])/g, (_, letra) => letra.toUpperCase())] ?? fallback
}

function GraficoConsumo({ items, moneda }) {
  const W = 800
  const H = 200
  const P = { top: 16, right: 12, bottom: 30, left: 46 }
  const innerW = W - P.left - P.right
  const innerH = H - P.top - P.bottom

  const maxConsumo = Math.max(...items.map((i) => Number(valorEntrada(i, 'consumo_kwh', 0)), 1))
  const escala = (v) => (v / maxConsumo) * innerH
  const paso = innerW / items.length
  const anchoBarra = Math.min(paso * 0.55, 54)

  const ticks = [0, 0.5, 1].map((f) => Math.round(maxConsumo * f))

  return (
    <svg className="chart" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet"
      role="img" aria-label="Consumo por analisis">
      {ticks.map((t, i) => {
        const y = P.top + innerH - escala(t)
        return (
          <g key={i}>
            <line x1={P.left} y1={y} x2={W - P.right} y2={y}
              stroke="var(--line)" strokeWidth="1" />
            <text x={P.left - 8} y={y + 4} textAnchor="end"
              fontSize="11" fill="var(--muted)">{t}</text>
          </g>
        )
      })}

      {items.map((item, i) => {
        const valor = Number(valorEntrada(item, 'consumo_kwh', 0))
        const h = escala(valor)
        const x = P.left + paso * i + (paso - anchoBarra) / 2
        const y = P.top + innerH - h
        return (
          <g key={i}>
            <rect x={x} y={y} width={anchoBarra} height={Math.max(h, 2)} rx="4"
              fill={COLOR_CLASE[item.clase] ?? 'var(--muted)'} />
            <text x={x + anchoBarra / 2} y={y - 6} textAnchor="middle"
              fontSize="11" fontWeight="600" fill="var(--ink)">{valor}</text>
            <text x={x + anchoBarra / 2} y={H - 10} textAnchor="middle"
              fontSize="11" fill="var(--muted)">
              {moneda}{Number(item.costoEstimadoMensual).toFixed(0)}
            </text>
          </g>
        )
      })}
    </svg>
  )
}

export default function Historial({ items, moneda, onLimpiar }) {
  const hay = items.length > 0

  const promedio = hay
    ? items.reduce((a, i) => a + Number(valorEntrada(i, 'consumo_kwh', 0)), 0) / items.length
    : 0
  const costoTotal = hay
    ? items.reduce((a, i) => a + Number(i.costoEstimadoMensual || 0), 0)
    : 0

  return (
    <div className="historial">
      <div className="section-head">
        <div>
          <h2>Historial y Seguimiento</h2>
          <p className="tag" style={{ margin: 0 }}>
            {hay
              ? `${items.length} analisis - consumo promedio ${promedio.toFixed(0)} kWh - costo acumulado ${moneda}${costoTotal.toFixed(2)}`
              : 'Aun no hay analisis registrados en esta sesion.'}
          </p>
        </div>
        {hay && onLimpiar && (
          <button type="button" className="linkbtn" onClick={onLimpiar}>
            Limpiar historial
          </button>
        )}
      </div>

      <div className="rcard">
        {hay ? (
          <>
            <GraficoConsumo items={items} moneda={moneda} />
            <table className="hist">
              <thead>
                <tr>
                  <th>Fecha</th>
                  <th>Inmueble</th>
                  <th>Consumo</th>
                  <th>Equipos</th>
                  <th>Pico</th>
                  <th>Perfil</th>
                  <th>Costo</th>
                </tr>
              </thead>
              <tbody>
                {[...items].reverse().map((item, i) => (
                  <tr key={i}>
                    <td>{new Date(item.fecha).toLocaleString('es-MX', {
                      day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit',
                    })}</td>
                    <td>{valorEntrada(item, 'tipo_inmueble', '-')}</td>
                    <td>{valorEntrada(item, 'consumo_kwh', '-')} kWh</td>
                    <td>{valorEntrada(item, 'cantidad_equipos', '-')}</td>
                    <td>{valorEntrada(item, 'uso_horario_pico', false) ? 'Si' : 'No'}</td>
                    <td><span className={`badge ${item.clase}`}>{item.categoria}</span></td>
                    <td>{moneda}{Number(item.costoEstimadoMensual).toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        ) : (
          <p className="chart-empty">
            Ejecuta un analisis para comenzar a dar seguimiento a tus indicadores
            de eficiencia a lo largo del tiempo.
          </p>
        )}
      </div>
    </div>
  )
}
