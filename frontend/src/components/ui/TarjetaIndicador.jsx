export default function TarjetaIndicador({ etiqueta, valor, detalle, tono = "azul", Icono, cargando = false }) {
  return (
    <article className={`indicador indicador--${tono}`}>
      <div className="indicador__cabecera">
        <span className="indicador__etiqueta">{etiqueta}</span>
        {Icono && (
          <span className="indicador__icono" aria-hidden="true">
            <Icono tamano={18} />
          </span>
        )}
      </div>

      {cargando ? (
        <span className="esqueleto__bloque esqueleto__bloque--numero" aria-hidden="true" />
      ) : (
        <p className="indicador__valor">{valor}</p>
      )}

      <p className="indicador__detalle">{detalle}</p>
    </article>
  );
}
