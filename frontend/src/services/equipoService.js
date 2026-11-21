import { api } from "./api.js";

export const equipoService = {
  listar({ texto = "", categoria = "", estado = "" } = {}) {
    const parametros = new URLSearchParams();
    if (texto.trim()) parametros.set("texto", texto.trim());
    if (categoria) parametros.set("categoria", categoria);
    if (estado) parametros.set("estado", estado);
    return api.obtener(`/equipos?${parametros.toString()}`);
  },

  todos() {
    return api.obtener("/equipos/todos");
  },

  crear(dto) {
    return api.crear("/equipos", dto);
  },

  actualizar(id, dto) {
    return api.reemplazar(`/equipos/${id}`, dto);
  },

  cambiarEstado(id, estado) {
    return api.actualizar(`/equipos/${id}/estado`, { estado });
  },

  eliminar(id) {
    return api.eliminar(`/equipos/${id}`);
  },
};
