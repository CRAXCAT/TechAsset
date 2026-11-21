const TONOS = {
  Administrador: "azul",
  Responsable: "verde",
  Colaborador: "gris",
};

export default function EtiquetaRol({ rol }) {
  const tono = TONOS[rol] ?? "gris";
  return <span className={`etiqueta etiqueta--${tono}`}>{rol}</span>;
}
