import { api } from "./api.js";

export const usuarioService = {
  listar({ texto = "", area = "", rol = "", activo = "" } = {}) {
    const parametros = new URLSearchParams();
    if (texto.trim()) parametros.set("texto", texto.trim());
    if (area) parametros.set("area", area);
    if (rol) parametros.set("rol", rol);
    if (activo !== "") parametros.set("activo", activo);
    return api.obtener(`/usuarios?${parametros.toString()}`);
  },

  crear(dto) {
    return api.crear("/usuarios", dto);
  },

  actualizar(id, dto) {
    return api.reemplazar(`/usuarios/${id}`, dto);
  },

  cambiarActivo(id, activo) {
    return api.actualizar(`/usuarios/${id}/activo?activo=${activo}`);
  },
};
