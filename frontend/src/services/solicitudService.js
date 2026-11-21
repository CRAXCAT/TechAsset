import { api } from "./api.js";

export const solicitudService = {
  listar({
    texto = "",
    estado = "",
    area = "",
    equipoId = "",
    pagina = 1,
    tamanoPagina = 8,
  } = {}) {
    const parametros = new URLSearchParams();
    if (texto.trim()) parametros.set("texto", texto.trim());
    if (estado) parametros.set("estado", estado);
    if (area) parametros.set("area", area);
    if (equipoId) parametros.set("equipoId", equipoId);
    parametros.set("pagina", String(pagina));
    parametros.set("tamanoPagina", String(tamanoPagina));
    return api.obtener(`/solicitudes?${parametros.toString()}`);
  },

  crear(dto) {
    return api.crear("/solicitudes", dto);
  },

  aprobar(id, observacionRevision = "") {
    return api.actualizar(`/solicitudes/${id}/aprobar`, { observacionRevision });
  },

  rechazar(id, observacionRevision) {
    return api.actualizar(`/solicitudes/${id}/rechazar`, { observacionRevision });
  },
};
