import { api } from "./api.js";

export const authService = {
  login({ correo, clave }) {
    return api.crear("/auth/login", { correo, clave });
  },

  cambiarClave({ claveActual, claveNueva }) {
    return api.crear("/auth/cambiar-clave", { claveActual, claveNueva });
  },
};
