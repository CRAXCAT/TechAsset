/**
 * Barras horizontales proporcionales. Se usan en el dashboard y en reportes
 * para equipos por estado, préstamos por área y equipos más utilizados.
 */
export default function BarrasDatos({ datos, vacio = "Sin datos disponibles." }) {
  if (!datos || datos.length === 0) {
    return <p className="vacio-compacto">{vacio}</p>;
  }

  const maximo = Math.max(...datos.map((d) => d.total), 1);
  const visibles = datos.slice(0, 7);

  return (
    <ul className="barras" aria-label="Distribución de datos">
      {visibles.map((dato) => (
        <li key={dato.etiqueta} className="barras__fila">
          <span className="barras__etiqueta" title={dato.etiqueta}>
            {dato.etiqueta}
          </span>
          <span className="barras__pista">
            <span className="barras__relleno" style={{ width: `${Math.max(6, (dato.total / maximo) * 100)}%` }} />
          </span>
          <span className="barras__valor">
            {dato.total} <span className="visualmente-oculto">registros</span>
          </span>
        </li>
      ))}
    </ul>
  );
}
