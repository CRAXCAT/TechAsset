import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext.jsx";
import { iniciales } from "../../utils/formato.js";
import {
  IconoAyuda,
  IconoGrafico,
  IconoInicio,
  IconoLaptop,
  IconoLista,
  IconoNuevo,
  IconoReloj,
  IconoSalir,
  IconoTicket,
  IconoSol,
  IconoLuna,
  IconoUsuarios,
} from "../ui/Iconos.jsx";

function enlacesPara(esGestor) {
  const base = [
    { ruta: "/panel", etiqueta: "Inicio", descripcion: "Panel de control", Icono: IconoInicio, fin: true },
  ];

  if (esGestor) {
    base.push({ ruta: "/usuarios", etiqueta: "Usuarios", descripcion: "Colaboradores y roles", Icono: IconoUsuarios });
  }

  base.push(
    { ruta: "/equipos", etiqueta: "Equipos", descripcion: "Inventario tecnológico", Icono: IconoLaptop },
    {
      ruta: "/solicitudes",
      etiqueta: esGestor ? "Solicitudes" : "Mis solicitudes",
      descripcion: esGestor ? "Revisión y aprobación" : "Estado de mis pedidos",
      Icono: IconoTicket,
      fin: true,
    },
    {
      ruta: "/prestamos",
      etiqueta: esGestor ? "Préstamos" : "Mi historial",
      descripcion: esGestor ? "Activos e historial" : "Mis préstamos",
      Icono: IconoLista,
      fin: true,
    },
  );

  if (esGestor) {
    base.push(
      { ruta: "/prestamos/nuevo", etiqueta: "Nuevo préstamo", descripcion: "Módulo de entrada", Icono: IconoNuevo },
      { ruta: "/reportes", etiqueta: "Reportes", descripcion: "Consultas e indicadores", Icono: IconoGrafico },
      { ruta: "/movimientos", etiqueta: "Movimientos", descripcion: "Auditoría de operaciones", Icono: IconoReloj },
    );
  }

  return base;
}

export default function Sidebar({ abierto, alCerrar, tema, alAlternarTema, alAbrirAyuda }) {
  const { usuario, logout } = useAuth();
  const navegar = useNavigate();
  const esGestor = usuario?.rol === "Administrador" || usuario?.rol === "Responsable";
  const enlaces = enlacesPara(esGestor);

  const cerrarSesion = () => {
    logout();
    navegar("/login", { replace: true });
  };

  return (
    <aside className={`barra-lateral ${abierto ? "barra-lateral--abierta" : ""}`} aria-label="Navegación principal">
      <div className="barra-lateral__marca">
        <span className="barra-lateral__logo" aria-hidden="true">
          <IconoLaptop />
        </span>
        <span className="barra-lateral__texto">
          <strong>TechAsset</strong>
          <small>INNOVATECH</small>
        </span>
      </div>

      <nav className="menu">
        <p className="menu__titulo">Operaciones</p>
        <ul className="menu__lista">
          {enlaces.map(({ ruta, etiqueta, descripcion, Icono, fin }) => (
            <li key={ruta}>
              <NavLink
                to={ruta}
                end={fin}
                className={({ isActive }) => `menu__enlace ${isActive ? "menu__enlace--activo" : ""}`}
                onClick={alCerrar}
              >
                <span className="menu__icono" aria-hidden="true">
                  <Icono />
                </span>
                <span className="menu__etiquetas">
                  <span className="menu__etiqueta">{etiqueta}</span>
                  <span className="menu__descripcion">{descripcion}</span>
                </span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      <div className="barra-lateral__pie">
        <button type="button" className="boton-tema" onClick={alAbrirAyuda}>
          <span aria-hidden="true">
            <IconoAyuda />
          </span>
          <span>Ayuda y atajos</span>
        </button>

        <button
          type="button"
          className="boton-tema"
          onClick={alAlternarTema}
          aria-pressed={tema === "oscuro"}
          title={tema === "oscuro" ? "Cambiar a tema claro" : "Cambiar a tema oscuro"}
        >
          <span aria-hidden="true">{tema === "oscuro" ? <IconoSol /> : <IconoLuna />}</span>
          <span>{tema === "oscuro" ? "Tema claro" : "Tema oscuro"}</span>
        </button>

        <div className="usuario">
          <span className="usuario__avatar" aria-hidden="true">
            {iniciales(usuario?.nombreCompleto ?? "")}
          </span>
          <span className="usuario__datos">
            <strong>{usuario?.nombreCompleto ?? "Sin sesión"}</strong>
            <small>{usuario?.rol ?? ""}</small>
          </span>
        </div>

        <div className="sesion-acciones">
          <NavLink to="/cambiar-clave" className="sesion-acciones__enlace" onClick={alCerrar}>
            Cambiar contraseña
          </NavLink>
          <button type="button" className="sesion-acciones__salir" onClick={cerrarSesion}>
            <IconoSalir tamano={16} />
            Cerrar sesión
          </button>
        </div>

        <p className="barra-lateral__version">Versión 1.0 · TechAsset</p>
      </div>
    </aside>
  );
}
