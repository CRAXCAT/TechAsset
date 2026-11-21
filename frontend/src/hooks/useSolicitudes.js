import { useCallback, useEffect, useState } from "react";
import { solicitudService } from "../services/solicitudService.js";

export function useSolicitudes({ texto, estado, area, equipoId, pagina, tamanoPagina }) {
  const [datos, setDatos] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);
  const [version, setVersion] = useState(0);

  useEffect(() => {
    let vigente = true;
    setCargando(true);
    setError(null);

    solicitudService
      .listar({ texto, estado, area, equipoId, pagina, tamanoPagina })
      .then((respuesta) => vigente && setDatos(respuesta))
      .catch((fallo) => {
        if (vigente) {
          setDatos(null);
          setError(fallo.message);
        }
      })
      .finally(() => vigente && setCargando(false));

    return () => {
      vigente = false;
    };
  }, [texto, estado, area, equipoId, pagina, tamanoPagina, version]);

  const recargar = useCallback(() => setVersion((actual) => actual + 1), []);
  return { datos, cargando, error, recargar };
}
