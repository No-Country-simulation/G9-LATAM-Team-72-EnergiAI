/**
 * Gauge semicircular con las tres zonas del perfil energetico.
 * La aguja se posiciona por categoria y se ajusta con la probabilidad del modelo.
 */
function anguloAguja(clase, probabilidad) {
  const p = Math.min(Math.max(Number(probabilidad) || 0, 0), 1)
  if (clase === 'ok') return -65 + (1 - p) * 20
  if (clase === 'mid') return -8 + (1 - p) * 16
  return 38 + p * 32
}

export default function GaugePerfil({ categoria, clase, probabilidad }) {
  const angulo = anguloAguja(clase, probabilidad)
  return (
    <>
      <svg
        className="gauge"
        viewBox="0 0 200 118"
        role="img"
        aria-label={`Perfil energetico: ${categoria}, probabilidad ${Math.round(probabilidad * 100)}%`}
      >
        <path d="M14 100 A86 86 0 0 1 60 26" fill="none" stroke="var(--ok)" strokeWidth="16" strokeLinecap="round" />
        <path d="M70 21 A86 86 0 0 1 130 21" fill="none" stroke="var(--mid)" strokeWidth="16" strokeLinecap="round" />
        <path d="M140 26 A86 86 0 0 1 186 100" fill="none" stroke="var(--bad)" strokeWidth="16" strokeLinecap="round" />
        <g className="needle" style={{ transform: `rotate(${angulo}deg)` }}>
          <line x1="100" y1="100" x2="100" y2="34" stroke="#334155" strokeWidth="4" strokeLinecap="round" />
        </g>
        <circle cx="100" cy="100" r="7" fill="#334155" />
      </svg>
      <div className={`cat ${clase}`}>{categoria}</div>
      <div className="prob">Probabilidad: {Math.round(probabilidad * 100)}%</div>
    </>
  )
}
