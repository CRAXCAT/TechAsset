import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

/**
 * Protege las rutas privadas: sin sesión redirige al login y, si el usuario
 * tiene una contraseña temporal, lo obliga a cambiarla antes de continuar.
 */
export default function RutaPrivada({ children }) {
  const { sesion, debeCambiarClave } = useAuth();
  const ubicacion = useLocation();

  if (!sesion) {
    return <Navigate to="/login" replace state={{ desde: ubicacion.pathname }} />;
  }

  if (debeCambiarClave && ubicacion.pathname !== "/cambiar-clave") {
    return <Navigate to="/cambiar-clave" replace />;
  }

  return children;
}
