/**
 * Tabla reutilizable para usuarios, equipos y préstamos. En móvil cada fila se
 * convierte en tarjeta con etiquetas, sin duplicar el componente por módulo.
 */
export default function TablaDatos({ columnas, filas, claveFila, tituloOculto }) {
  return (
    <div className="tabla-envoltura">
      <table className="tabla">
        <caption className="visualmente-oculto">{tituloOculto}</caption>
        <thead>
          <tr>
            {columnas.map((columna) => (
              <th key={columna.clave} scope="col" className={columna.clase}>
                {columna.titulo}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {filas.map((fila) => (
            <tr key={claveFila(fila)}>
              {columnas.map((columna) => (
                <td key={columna.clave} data-etiqueta={columna.titulo} className={columna.clase}>
                  {columna.render ? columna.render(fila) : fila[columna.clave]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
