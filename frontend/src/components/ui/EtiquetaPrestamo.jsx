import { TONO_PRESTAMO } from "../../utils/constantes.js";

export default function EtiquetaPrestamo({ estado }) {
  const tono = TONO_PRESTAMO[estado] ?? "gris";
  return (
    <span className={`etiqueta etiqueta--${tono}`}>
      <span className="etiqueta__punto" aria-hidden="true" />
      {estado}
    </span>
  );
}
