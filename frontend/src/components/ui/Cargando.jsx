/**
 * Esqueleto de carga: comunica que el sistema está trabajando sin mostrar
 * una pantalla vacía (visibilidad del estado del sistema).
 */
export default function Cargando({ filas = 4, etiqueta = "Cargando información" }) {
  return (
    <div className="esqueleto" role="status" aria-live="polite" aria-busy="true">
      <span className="visualmente-oculto">{etiqueta}...</span>
      {Array.from({ length: filas }).map((_, indice) => (
        <div key={indice} className="esqueleto__fila" aria-hidden="true">
          <span className="esqueleto__bloque esqueleto__bloque--corto" />
          <span className="esqueleto__bloque" />
          <span className="esqueleto__bloque esqueleto__bloque--medio" />
        </div>
      ))}
    </div>
  );
}
