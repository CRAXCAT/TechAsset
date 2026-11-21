import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { authService } from "../services/authService.js";

const CLAVE = "techasset-sesion";
const ContextoAuth = createContext(null);

function leerSesion() {
  try {
    const datos = JSON.parse(localStorage.getItem(CLAVE));
    return datos?.token ? datos : null;
  } catch {
    return null;
  }
}

/**
 * Sesión del usuario autenticado. Guarda el token JWT y los datos del usuario
 * en localStorage para conservar la sesión entre recargas.
 */
export function ProveedorAuth({ children }) {
  const [sesion, setSesion] = useState(leerSesion);

  const login = useCallback(async (correo, clave) => {
    const datos = await authService.login({ correo, clave });
    localStorage.setItem(CLAVE, JSON.stringify(datos));
    setSesion(datos);
    return datos;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem(CLAVE);
    setSesion(null);
  }, []);

  const actualizarUsuario = useCallback((usuario) => {
    setSesion((actual) => {
      if (!actual) return actual;
      const siguiente = { ...actual, usuario };
      localStorage.setItem(CLAVE, JSON.stringify(siguiente));
      return siguiente;
    });
  }, []);

  // El cliente API avisa cuando el token expira o es rechazado.
  useEffect(() => {
    const alExpirar = () => logout();
    window.addEventListener("sesion-expirada", alExpirar);
    return () => window.removeEventListener("sesion-expirada", alExpirar);
  }, [logout]);

  const valor = useMemo(() => {
    const usuario = sesion?.usuario ?? null;
    return {
      sesion,
      token: sesion?.token ?? null,
      usuario,
      login,
      logout,
      actualizarUsuario,
      esAdministrador: usuario?.rol === "Administrador",
      debeCambiarClave: Boolean(usuario?.debeCambiarPassword),
    };
  }, [sesion, login, logout, actualizarUsuario]);

  return <ContextoAuth.Provider value={valor}>{children}</ContextoAuth.Provider>;
}

export function useAuth() {
  const contexto = useContext(ContextoAuth);
  if (!contexto) throw new Error("useAuth debe usarse dentro de ProveedorAuth");
  return contexto;
}
