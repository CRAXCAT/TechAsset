import { useCallback, useEffect, useState } from "react";
import { equipoService } from "../services/equipoService.js";

export function useEquipos({ texto, categoria, estado }) {
  const [datos, setDatos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);
  const [version, setVersion] = useState(0);

  useEffect(() => {
    let vigente = true;
    setCargando(true);
    setError(null);

    equipoService
      .listar({ texto, categoria, estado })
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
  }, [texto, categoria, estado, version]);

  const recargar = useCallback(() => setVersion((actual) => actual + 1), []);
  return { datos, cargando, error, recargar };
}
