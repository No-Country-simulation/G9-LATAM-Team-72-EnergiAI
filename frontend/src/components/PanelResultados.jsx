import GaugePerfil from './GaugePerfil'

function EstadoVacio() {
  return (
    <div className="empty">
      <svg width="34" height="34" viewBox="0 0 24 24" fill="none"
        stroke="currentColor" strokeWidth="1.6" aria-hidden="true">
        <path d="M3 3v18h18" />
        <path d="M7 14l3-4 3 3 4-6" />
      </svg>
      <div>
        Completa los datos y presiona <b>Analizar mi perfil</b> para ver tu
        clasificacion, impacto financiero y recomendaciones.
      </div>
    </div>
  )
}

export default function PanelResultados({ resultado, error, tarifa, moneda }) {
  if (error) {
    return (
      <div className="results">
        <div className="alert">
          No se pudo completar el analisis: {error}. Revisa los datos o la
          conexion con el API e intentalo de nuevo.
        </div>
      </div>
    )
  }

  if (!resultado) {
    return (
      <div className="results">
        <EstadoVacio />
      </div>
    )
  }

  return (
    <div className="results">
      <div className="rcard gauge-wrap">
        <h3 style={{ alignSelf: 'flex-start' }}>Perfil Energetico Actual</h3>
        <GaugePerfil
          categoria={resultado.categoria}
          clase={resultado.clase}
          probabilidad={resultado.probabilidad}
        />
      </div>

      <div className="rcard">
        <h3>Impacto Financiero Estimado</h3>
        <p className="cost">
          {moneda}{resultado.costoEstimadoMensual.toFixed(2)}
          <small>mensual</small>
        </p>
        <div className="rate">
          <svg className="calc" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" strokeWidth="1.6" aria-hidden="true">
            <rect x="4" y="2" width="16" height="20" rx="2" />
            <path d="M8 6h8M8 10h2M12 10h4M8 14h2M12 14h4M8 18h8" />
          </svg>
          <span>Tarifa de referencia: {moneda}{tarifa.toFixed(2)} por kWh</span>
        </div>
      </div>

      <div className="rcard">
        <h3>Recomendaciones Personalizadas</h3>
        <ul className="recs">
          {resultado.recomendaciones.map((rec, i) => (
            <li key={i}>{rec}</li>
          ))}
        </ul>
      </div>
    </div>
  )
}
