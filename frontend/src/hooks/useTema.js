import { useCallback, useEffect, useState } from "react";

const CLAVE = "techasset-tema";

/**
 * Tema claro/oscuro persistido en el navegador. La preferencia se aplica al
 * documento mediante data-tema, de modo que el CSS controla toda la paleta.
 */
export function useTema() {
  const [tema, setTema] = useState(() => {
    const guardado = localStorage.getItem(CLAVE);
    if (guardado === "claro" || guardado === "oscuro") return guardado;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "oscuro" : "claro";
  });

  useEffect(() => {
    document.documentElement.dataset.tema = tema;
    localStorage.setItem(CLAVE, tema);
  }, [tema]);

  const alternarTema = useCallback(() => {
    setTema((actual) => (actual === "oscuro" ? "claro" : "oscuro"));
  }, []);

  return { tema, alternarTema };
}
