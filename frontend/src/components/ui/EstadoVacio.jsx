import { IconoTicket } from "./Iconos.jsx";

export default function EstadoVacio({ titulo, mensaje, accion }) {
  return (
    <div className="estado-vacio">
      <span className="estado-vacio__icono" aria-hidden="true">
        <IconoTicket tamano={28} />
      </span>
      <h3 className="estado-vacio__titulo">{titulo}</h3>
      <p className="estado-vacio__mensaje">{mensaje}</p>
      {accion}
    </div>
  );
}
