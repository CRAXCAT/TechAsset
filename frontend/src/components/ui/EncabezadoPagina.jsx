export default function EncabezadoPagina({ titulo, descripcion, acciones }) {
  return (
    <header className="encabezado">
      <div className="encabezado__texto">
        <h1 className="encabezado__titulo">{titulo}</h1>
        {descripcion && <p className="encabezado__descripcion">{descripcion}</p>}
      </div>
      {acciones && <div className="encabezado__acciones">{acciones}</div>}
    </header>
  );
}
