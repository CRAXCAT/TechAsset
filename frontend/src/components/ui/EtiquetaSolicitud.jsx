import { TONO_SOLICITUD } from "../../utils/constantes.js";

export default function EtiquetaSolicitud({ estado }) {
  const tono = TONO_SOLICITUD[estado] ?? "gris";
  return (
    <span className={`etiqueta etiqueta--${tono}`}>
      <span className="etiqueta__punto" aria-hidden="true" />
      {estado}
    </span>
  );
}
