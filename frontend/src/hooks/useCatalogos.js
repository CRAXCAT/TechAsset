import { useEffect, useState } from "react";
import { equipoService } from "../services/equipoService.js";
import { usuarioService } from "../services/usuarioService.js";

export function useCatalogos({ usuarios = true, equipos = true } = {}) {
  const [listaUsuarios, setListaUsuarios] = useState([]);
  const [listaEquipos, setListaEquipos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);
  const [version, setVersion] = useState(0);

  useEffect(() => {
    let vigente = true;
    setCargando(true);
    setError(null);

    Promise.all([
      usuarios ? usuarioService.listar() : Promise.resolve([]),
      equipos ? equipoService.todos() : Promise.resolve([]),
    ])
      .then(([datosUsuarios, datosEquipos]) => {
        if (!vigente) return;
        setListaUsuarios(datosUsuarios ?? []);
        setListaEquipos(datosEquipos ?? []);
      })
      .catch((fallo) => vigente && setError(fallo.message))
      .finally(() => vigente && setCargando(false));

    return () => {
      vigente = false;
    };
  }, [usuarios, equipos, version]);

  return {
    usuarios: listaUsuarios,
    equipos: listaEquipos,
    cargando,
    error,
    recargar: () => setVersion((actual) => actual + 1),
  };
}
