import { useCallback, useEffect, useState } from "react";
import { usuarioService } from "../services/usuarioService.js";

export function useUsuarios({ texto, area, rol, activo }) {
  const [datos, setDatos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);
  const [version, setVersion] = useState(0);

  useEffect(() => {
    let vigente = true;
    setCargando(true);
    setError(null);

    usuarioService
      .listar({ texto, area, rol, activo })
      .then((respuesta) => vigente && setDatos(respuesta ?? []))
      .catch((fallo) => {
        if (vigente) {
          setDatos([]);
          setError(fallo.message);
        }
      })
      .finally(() => vigente && setCargando(false));

    return () => {
      vigente = false;
    };
  }, [texto, area, rol, activo, version]);

  const recargar = useCallback(() => setVersion((actual) => actual + 1), []);
  return { datos, cargando, error, recargar };
}
