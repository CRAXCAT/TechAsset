import Modal from "./Modal.jsx";
import { IconoEscudo, IconoInfo, IconoTeclado } from "./Iconos.jsx";

const ATAJOS = [
  ["Alt", "I", "Ir al panel de control"],
  ["Alt", "U", "Abrir usuarios"],
  ["Alt", "E", "Abrir el inventario de equipos"],
  ["Alt", "S", "Abrir solicitudes"],
  ["Alt", "P", "Abrir préstamos"],
  ["Alt", "R", "Abrir reportes"],
  ["Alt", "M", "Abrir movimientos"],
  ["/", "", "Enfocar el buscador de la página"],
  ["?", "", "Abrir esta ayuda"],
  ["Esc", "", "Cerrar ventanas y confirmaciones"],
];

const REGLAS = [
  "Un equipo solo puede tener un préstamo activo (RN-01).",
  "No se prestan equipos en Mantenimiento ni en Baja (RN-02 y RN-03).",
  "La devolución debe ser posterior al préstamo (RN-04).",
  "Todo préstamo registra un responsable (RN-05).",
  "No se elimina un equipo con historial de préstamos (RN-06).",
  "Toda devolución exige observaciones (RN-10).",
  "Una solicitud pendiente por equipo; la aprobación genera el préstamo.",
];

export default function ModalAyuda({ abierto, alCerrar }) {
  return (
    <Modal
      abierto={abierto}
      alCerrar={alCerrar}
      titulo="Ayuda y atajos"
      descripcion="Use TechAsset con teclado y consulte las reglas sin memorizarlas."
      pie={
        <button type="button" className="boton boton--primario" onClick={alCerrar} data-autofocus>
          Entendido
        </button>
      }
    >
      <div className="ayuda">
        <section aria-labelledby="ayuda-atajos">
          <h3 id="ayuda-atajos" className="ayuda__titulo">
            <IconoTeclado tamano={18} /> Atajos de teclado
          </h3>
          <ul className="ayuda__atajos">
            {ATAJOS.map(([primera, segunda, detalle]) => (
              <li key={`${primera}-${detalle}`}>
                <span className="ayuda__teclas">
                  <kbd>{primera}</kbd>
                  {segunda && (
                    <>
                      <span aria-hidden="true"> + </span>
                      <kbd>{segunda}</kbd>
                    </>
                  )}
                </span>
                <span>{detalle}</span>
              </li>
            ))}
          </ul>
        </section>

        <section aria-labelledby="ayuda-reglas">
          <h3 id="ayuda-reglas" className="ayuda__titulo">
            <IconoEscudo tamano={18} /> Reglas del préstamo
          </h3>
          <ul className="ayuda__lista">
            {REGLAS.map((regla) => (
              <li key={regla}>{regla}</li>
            ))}
          </ul>
        </section>

        <section aria-labelledby="ayuda-accesibilidad">
          <h3 id="ayuda-accesibilidad" className="ayuda__titulo">
            <IconoInfo tamano={18} /> Accesibilidad
          </h3>
          <ul className="ayuda__lista">
            <li>El primer <kbd>Tab</kbd> lleva al contenido principal; el foco siempre es visible.</li>
            <li>Los formularios anuncian sus errores junto al campo y con lectores de pantalla.</li>
            <li>Las ventanas se cierran con <kbd>Esc</kbd> y devuelven el foco al botón de origen.</li>
            <li>El tema claro u oscuro se conserva en el navegador.</li>
          </ul>
        </section>
      </div>
    </Modal>
  );
}
