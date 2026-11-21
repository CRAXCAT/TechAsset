import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext.jsx";
import { prestamoService } from "../../services/prestamoService.js";
import EtiquetaRol from "../ui/EtiquetaRol.jsx";
import { IconoAyuda, IconoBaseDatos, IconoLuna, IconoMenu, IconoSalir, IconoSol } from "../ui/Iconos.jsx";

const TITULOS = {
  "/panel": "Panel de control",
  "/usuarios": "Usuarios",
  "/equipos": "Inventario de equipos",
  "/solicitudes": "Solicitudes",
  "/solicitudes/nueva": "Nueva solicitud",
  "/prestamos": "Préstamos",
  "/prestamos/nuevo": "Nuevo préstamo",
  "/reportes": "Reportes",
  "/movimientos": "Movimientos",
};

export default function Topbar({ alAbrirMenu, alAbrirAyuda, tema, alAlternarTema }) {
  const { pathname } = useLocation();
  const { usuario, logout } = useAuth();
  const navegar = useNavigate();
  const [estadoApi, setEstadoApi] = useState("verificando");

  useEffect(() => {
    let vigente = true;
    prestamoService
      .resumen()
      .then(() => vigente && setEstadoApi("en-linea"))
      .catch(() => vigente && setEstadoApi("sin-conexion"));
    return () => {
      vigente = false;
    };
  }, [pathname]);

  const titulo = TITULOS[pathname] ?? "Página no encontrada";
  const esInicio = pathname === "/panel";
  const seccion = pathname.startsWith("/usuarios")
    ? "Usuarios"
    : pathname.startsWith("/equipos")
      ? "Equipos"
      : pathname.startsWith("/solicitudes")
        ? "Solicitudes"
        : pathname.startsWith("/prestamos")
          ? "Préstamos"
          : pathname.startsWith("/reportes")
            ? "Reportes"
            : pathname.startsWith("/movimientos")
              ? "Movimientos"
              : "General";

  const cerrarSesion = () => {
    logout();
    navegar("/login", { replace: true });
  };

  return (
    <header className="barra-superior">
      <button
        type="button"
        className="boton-icono barra-superior__menu"
        onClick={alAbrirMenu}
        aria-label="Abrir el menú de navegación"
      >
        <IconoMenu />
      </button>

      <div className="migas" aria-label="Ubicación en el sistema">
        <Link to="/panel" className="migas__enlace">
          Inicio
        </Link>
        <span aria-hidden="true">/</span>
        {esInicio ? (
          <span aria-current="page">{titulo}</span>
        ) : (
          <>
            {seccion !== titulo && (
              <>
                <span>{seccion}</span>
                <span aria-hidden="true">/</span>
              </>
            )}
            <span aria-current="page">{titulo}</span>
          </>
        )}
      </div>

      <div className="barra-superior__acciones">
        <span className={`estado-api estado-api--${estadoApi}`} role="status">
          <IconoBaseDatos />
          {estadoApi === "en-linea" && "API y PostgreSQL en línea"}
          {estadoApi === "verificando" && "Verificando conexión..."}
          {estadoApi === "sin-conexion" && "Sin conexión con la API"}
        </span>

        {usuario && <EtiquetaRol rol={usuario.rol} />}

        <button
          type="button"
          className="boton-icono"
          onClick={alAbrirAyuda}
          aria-label="Ayuda y atajos"
          title="Ayuda y atajos"
        >
          <IconoAyuda />
        </button>

        <button
          type="button"
          className="boton-icono"
          onClick={alAlternarTema}
          aria-label={tema === "oscuro" ? "Cambiar a tema claro" : "Cambiar a tema oscuro"}
          aria-pressed={tema === "oscuro"}
        >
          {tema === "oscuro" ? <IconoSol /> : <IconoLuna />}
        </button>

        <button type="button" className="boton-icono" onClick={cerrarSesion} aria-label="Cerrar sesión">
          <IconoSalir />
        </button>
      </div>
    </header>
  );
}
