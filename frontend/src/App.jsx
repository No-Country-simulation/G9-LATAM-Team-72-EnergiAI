import { useEffect, useState } from 'react'
import TopBar from './components/TopBar'
import FormularioAnalisis from './components/FormularioAnalisis'
import PanelResultados from './components/PanelResultados'
import Historial from './components/Historial'
import { VALORES_INICIALES, validar } from './lib/escenarios'
import {
  analizarConsumo, despertarServicio,
  API_URL, USE_MOCK, TARIFA, MONEDA,
} from './api/energiai'

export default function App() {
  const [datos, setDatos] = useState(VALORES_INICIALES)
  const [errores, setErrores] = useState({})
  const [cargando, setCargando] = useState(false)
  const [resultado, setResultado] = useState(null)
  const [error, setError] = useState(null)
  const [historial, setHistorial] = useState([])
  const [escenarioActivo, setEscenarioActivo] = useState('enunciado')
  // 'desconocido' | 'despertando' | 'listo'  (solo aplica en modo API)
  const [estadoServicio, setEstadoServicio] = useState(USE_MOCK ? 'listo' : 'desconocido')

  // Warm-up del backend en Render (free tier se duerme y tarda 30-50s en frio).
  useEffect(() => {
    if (USE_MOCK) return
    let activo = true
    setEstadoServicio('despertando')
    despertarServicio().then((ok) => {
      if (activo) setEstadoServicio(ok ? 'listo' : 'desconocido')
    })
    return () => { activo = false }
  }, [])

  const cambiarCampo = (campo, valor) => {
    setDatos((prev) => ({ ...prev, [campo]: valor }))
    setEscenarioActivo(null)
    setErrores((prev) => ({ ...prev, [campo]: undefined }))
  }

  const cargarEscenario = (escenario) => {
    setDatos(escenario.datos)
    setEscenarioActivo(escenario.id)
    setErrores({})
  }

  const analizar = async () => {
    const errs = validar(datos)
    setErrores(errs)
    if (Object.keys(errs).length > 0) return

    setCargando(true)
    setError(null)
    try {
      const res = await analizarConsumo(datos)
      setResultado(res)
      setHistorial((prev) => [...prev, res])
      if (!USE_MOCK) setEstadoServicio('listo')
    } catch (e) {
      setError(e.message || 'error desconocido')
      setResultado(null)
    } finally {
      setCargando(false)
    }
  }

  const modo = USE_MOCK
    ? 'Simulador local'
    : estadoServicio === 'despertando'
      ? 'Despertando servicio...'
      : 'Conectado'

  return (
    <div className="app">
      <div className="shell">
        <TopBar modo={modo} />
        <div className="body">
          <h1 className="appname">
            <b>EnergiAI</b> - Inteligencia para el Consumo Energetico
          </h1>
          <p className="tag">Team 72 - Hackathon ONE G9 LATAM</p>

          {!USE_MOCK && estadoServicio === 'despertando' && (
            <div className="aviso">
              Contactando el servicio en Render. Si estaba inactivo, la primera
              respuesta puede tardar entre 30 y 50 segundos.
            </div>
          )}

          <FormularioAnalisis
            datos={datos}
            errores={errores}
            cargando={cargando}
            escenarioActivo={escenarioActivo}
            onCambio={cambiarCampo}
            onEscenario={cargarEscenario}
            onAnalizar={analizar}
          />

          <PanelResultados
            resultado={resultado}
            error={error}
            tarifa={TARIFA}
            moneda={MONEDA}
          />

          <Historial
            items={historial}
            moneda={MONEDA}
            onLimpiar={() => setHistorial([])}
          />
        </div>
      </div>
    </div>
  )
}
