import { api } from "./api.js";

export const prestamoService = {
  listar({
    texto = "",
    estado = "",
    area = "",
    equipoId = "",
    desde = "",
    hasta = "",
    pagina = 1,
    tamanoPagina = 8,
  } = {}) {
    const parametros = new URLSearchParams();
    if (texto.trim()) parametros.set("texto", texto.trim());
    if (estado) parametros.set("estado", estado);
    if (area) parametros.set("area", area);
    if (equipoId) parametros.set("equipoId", equipoId);
    if (desde) parametros.set("desde", desde);
    if (hasta) parametros.set("hasta", hasta);
    parametros.set("pagina", String(pagina));
    parametros.set("tamanoPagina", String(tamanoPagina));
    return api.obtener(`/prestamos?${parametros.toString()}`);
  },

  obtener(id) {
    return api.obtener(`/prestamos/${id}`);
  },

  crear(dto) {
    return api.crear("/prestamos", dto);
  },

  devolver(id, observacionDevolucion) {
    return api.actualizar(`/prestamos/${id}/devolver`, { observacionDevolucion });
  },

  resumen() {
    return api.obtener("/reportes/resumen");
  },
};
