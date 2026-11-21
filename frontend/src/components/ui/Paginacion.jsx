import { IconoFlechaIzquierda, IconoFlechaDerecha } from "./Iconos.jsx";

function rangoPaginas(actual, total) {
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1);

  const paginas = new Set([1, total, actual, actual - 1, actual + 1]);
  const ordenadas = [...paginas].filter((p) => p >= 1 && p <= total).sort((a, b) => a - b);

  const resultado = [];
  ordenadas.forEach((pagina, indice) => {
    if (indice > 0 && pagina - ordenadas[indice - 1] > 1) resultado.push("…");
    resultado.push(pagina);
  });

  return resultado;
}

export default function Paginacion({ pagina, totalPaginas, total, desde, hasta, alCambiar, sustantivo = "registros" }) {
  if (total === 0) return null;

  const paginas = rangoPaginas(pagina, totalPaginas);

  return (
    <nav className="paginacion" aria-label="Paginación del listado">
      <p className="paginacion__resumen">
        Mostrando <strong>{desde}</strong>–<strong>{hasta}</strong> de <strong>{total}</strong> {sustantivo}
      </p>

      <div className="paginacion__controles">
        <button
          type="button"
          className="paginacion__boton"
          onClick={() => alCambiar(pagina - 1)}
          disabled={pagina <= 1}
          aria-label="Ir a la página anterior"
        >
          <IconoFlechaIzquierda tamano={16} />
        </button>

        {paginas.map((numero, indice) =>
          numero === "…" ? (
            <span key={`separador-${indice}`} className="paginacion__separador" aria-hidden="true">
              …
            </span>
          ) : (
            <button
              key={numero}
              type="button"
              className={`paginacion__boton ${numero === pagina ? "paginacion__boton--activo" : ""}`}
              onClick={() => alCambiar(numero)}
              aria-label={`Ir a la página ${numero}`}
              aria-current={numero === pagina ? "page" : undefined}
            >
              {numero}
            </button>
          )
        )}

        <button
          type="button"
          className="paginacion__boton"
          onClick={() => alCambiar(pagina + 1)}
          disabled={pagina >= totalPaginas}
          aria-label="Ir a la página siguiente"
        >
          <IconoFlechaDerecha tamano={16} />
        </button>
      </div>
    </nav>
  );
}
