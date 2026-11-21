import { TONO_EQUIPO } from "../../utils/constantes.js";

export default function EtiquetaEquipo({ estado }) {
  const tono = TONO_EQUIPO[estado] ?? "gris";
  return (
    <span className={`etiqueta etiqueta--${tono}`}>
      <span className="etiqueta__punto" aria-hidden="true" />
      {estado}
    </span>
  );
}
