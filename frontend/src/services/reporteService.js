import { api } from "./api.js";

export const reporteService = {
  resumen() {
    return api.obtener("/reportes/resumen");
  },

  descargarPrestamos(filtros = {}) {
    const parametros = new URLSearchParams();
    if (filtros.estado) parametros.set("estado", filtros.estado);
    if (filtros.area) parametros.set("area", filtros.area);
    if (filtros.desde) parametros.set("desde", filtros.desde);
    if (filtros.hasta) parametros.set("hasta", filtros.hasta);
    return api.descargar(`/reportes/prestamos.csv?${parametros.toString()}`);
  },

  descargarEquipos(filtros = {}) {
    const parametros = new URLSearchParams();
    if (filtros.categoria) parametros.set("categoria", filtros.categoria);
    if (filtros.estado) parametros.set("estado", filtros.estado);
    return api.descargar(`/reportes/equipos.csv?${parametros.toString()}`);
  },
};
