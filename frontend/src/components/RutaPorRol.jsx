import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

/** Restringe una ruta a los roles indicados; el servidor vuelve a validar los permisos. */
export default function RutaPorRol({ roles, children }) {
  const { usuario } = useAuth();

  if (!usuario || !roles.includes(usuario.rol)) {
    return <Navigate to="/panel" replace />;
  }

  return children;
}
