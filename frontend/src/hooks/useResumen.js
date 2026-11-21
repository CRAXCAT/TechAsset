import { useCallback, useEffect, useState } from "react";
import { prestamoService } from "../services/prestamoService.js";

export function useResumen() {
  const [resumen, setResumen] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);
  const [version, setVersion] = useState(0);

  useEffect(() => {
    let vigente = true;
    setCargando(true);
    setError(null);

    prestamoService
      .resumen()
      .then((datos) => vigente && setResumen(datos))
      .catch((fallo) => vigente && setError(fallo.message))
      .finally(() => vigente && setCargando(false));

    return () => {
      vigente = false;
    };
  }, [version]);

  const recargar = useCallback(() => setVersion((actual) => actual + 1), []);
  return { resumen, cargando, error, recargar };
}
