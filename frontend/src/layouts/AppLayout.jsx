import { useEffect, useState } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import Sidebar from "../components/layout/Sidebar.jsx";
import Topbar from "../components/layout/Topbar.jsx";
import ModalAyuda from "../components/ui/ModalAyuda.jsx";
import { useTema } from "../hooks/useTema.js";

/**
 * Layout único de la aplicación: barra lateral, barra superior y contenido.
 * Además centraliza los atajos de teclado y la ayuda accesible.
 */
export default function AppLayout() {
  const [menuAbierto, setMenuAbierto] = useState(false);
  const [ayudaAbierta, setAyudaAbierta] = useState(false);
  const { tema, alternarTema } = useTema();
  const { pathname } = useLocation();
  const navegar = useNavigate();

  useEffect(() => {
    setMenuAbierto(false);
  }, [pathname]);

  useEffect(() => {
    if (!menuAbierto) return undefined;

    const alPresionarTecla = (evento) => {
      if (evento.key === "Escape") setMenuAbierto(false);
    };

    document.body.classList.add("sin-scroll");
    window.addEventListener("keydown", alPresionarTecla);

    return () => {
      document.body.classList.remove("sin-scroll");
      window.removeEventListener("keydown", alPresionarTecla);
    };
  }, [menuAbierto]);

  useEffect(() => {
    const alPresionarTecla = (evento) => {
      const etiqueta = evento.target?.tagName ?? "";
      const escribiendo =
        ["INPUT", "TEXTAREA", "SELECT"].includes(etiqueta) || evento.target?.isContentEditable;

      if (evento.altKey && !evento.ctrlKey && !evento.metaKey) {
        const tecla = evento.key.toLowerCase();
        if (tecla === "i") {
          evento.preventDefault();
          navegar("/panel");
        } else if (tecla === "u") {
          evento.preventDefault();
          navegar("/usuarios");
        } else if (tecla === "e") {
          evento.preventDefault();
          navegar("/equipos");
        } else if (tecla === "p") {
          evento.preventDefault();
          navegar("/prestamos");
        } else if (tecla === "s") {
          evento.preventDefault();
          navegar("/solicitudes");
        } else if (tecla === "r") {
          evento.preventDefault();
          navegar("/reportes");
        } else if (tecla === "m") {
          evento.preventDefault();
          navegar("/movimientos");
        }
      }

      if (!escribiendo && evento.key === "/") {
        const buscador = document.querySelector("#busqueda, #busqueda-usuario");
        if (buscador) {
          evento.preventDefault();
          buscador.focus();
          buscador.select?.();
        }
      }

      if (!escribiendo && evento.key === "?") {
        evento.preventDefault();
        setAyudaAbierta(true);
      }
    };

    window.addEventListener("keydown", alPresionarTecla);
    return () => window.removeEventListener("keydown", alPresionarTecla);
  }, [navegar]);

  return (
    <div className="aplicacion">
      <a className="enlace-salto" href="#contenido">
        Ir al contenido principal
      </a>

      <Sidebar
        abierto={menuAbierto}
        alCerrar={() => setMenuAbierto(false)}
        tema={tema}
        alAlternarTema={alternarTema}
        alAbrirAyuda={() => setAyudaAbierta(true)}
      />

      {menuAbierto && (
        <button
          type="button"
          className="telon"
          aria-label="Cerrar el menú de navegación"
          onClick={() => setMenuAbierto(false)}
        />
      )}

      <div className="aplicacion__cuerpo">
        <Topbar
          alAbrirMenu={() => setMenuAbierto(true)}
          alAbrirAyuda={() => setAyudaAbierta(true)}
          tema={tema}
          alAlternarTema={alternarTema}
        />

        <main id="contenido" className="contenido" tabIndex={-1}>
          <Outlet />
        </main>

        <footer className="pie">
          <span>TechAsset · Inventario y préstamo de equipos tecnológicos</span>
          <span>Construcción de Software · Innovatech Solutions</span>
        </footer>
      </div>

      <ModalAyuda abierto={ayudaAbierta} alCerrar={() => setAyudaAbierta(false)} />
    </div>
  );
}
