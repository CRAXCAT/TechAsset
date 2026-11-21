import { api } from "./api.js";

export const movimientoService = {
  listar({ texto = "", entidad = "", accion = "", pagina = 1, tamanoPagina = 12 } = {}) {
    const parametros = new URLSearchParams();
    if (texto.trim()) parametros.set("texto", texto.trim());
    if (entidad) parametros.set("entidad", entidad);
    if (accion) parametros.set("accion", accion);
    parametros.set("pagina", String(pagina));
    parametros.set("tamanoPagina", String(tamanoPagina));
    return api.obtener(`/movimientos?${parametros.toString()}`);
  },
};
