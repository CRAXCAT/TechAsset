import { Link } from "react-router-dom";
import {
  IconoAlerta,
  IconoBaseDatos,
  IconoCheck,
  IconoDevolver,
  IconoEscudo,
  IconoFlechaDerecha,
  IconoGrafico,
  IconoLaptop,
  IconoLuna,
  IconoReloj,
  IconoSol,
  IconoUsuarios,
} from "../components/ui/Iconos.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { useTema } from "../hooks/useTema.js";

const FUNCIONES = [
  {
    Icono: IconoLaptop,
    titulo: "Inventario centralizado",
    texto: "Laptops, monitores, impresoras, tablets, proyectores y equipos de red en un solo registro con código patrimonial único.",
  },
  {
    Icono: IconoDevolver,
    titulo: "Préstamos con trazabilidad",
    texto: "Cada entrega registra colaborador, responsable, fechas y motivo; la devolución exige observaciones.",
  },
  {
    Icono: IconoUsuarios,
    titulo: "Usuarios y roles",
    texto: "Administrador, Responsable de Tecnología y Colaborador, con permisos verificados en el servidor.",
  },
  {
    Icono: IconoGrafico,
    titulo: "Reportes e indicadores",
    texto: "Dashboard con seis indicadores, equipos por estado, préstamos por área y ranking de equipos más utilizados.",
  },
  {
    Icono: IconoBaseDatos,
    titulo: "Datos consistentes",
    texto: "PostgreSQL y transacciones: el préstamo y el estado del equipo se confirman juntos o no se confirman.",
  },
  {
    Icono: IconoEscudo,
    titulo: "Acceso seguro",
    texto: "Contraseñas con BCrypt, sesiones JWT, contraseña temporal y rutas privadas por rol.",
  },
];

const PASOS = [
  {
    numero: "01",
    titulo: "Registra el equipo",
    texto: "El Administrador o el Responsable dan de alta el activo con su código patrimonial, categoría, marca y estado.",
  },
  {
    numero: "02",
    titulo: "Asigna el préstamo",
    texto: "Se elige un colaborador activo y un equipo disponible; el sistema valida las diez reglas antes de guardar.",
  },
  {
    numero: "03",
    titulo: "Controla la devolución",
    texto: "Al devolver, el equipo vuelve a Disponible y queda la fecha real y la observación para auditoría.",
  },
];

const BENEFICIOS = [
  "Sin duplicidad de registros",
  "Disponibilidad en tiempo real",
  "Historial por colaborador y equipo",
];

export default function Inicio() {
  const { sesion, logout } = useAuth();
  const { tema, alternarTema } = useTema();

  return (
    <div className="portal">
      <a className="enlace-salto" href="#contenido">
        Ir al contenido principal
      </a>

      <header className="portal__cabecera">
        <div className="portal__contenedor portal__cabecera-fila">
          <Link to="/" className="portal__marca" aria-label="TechAsset, ir al inicio">
            <span className="portal__logo" aria-hidden="true">
              <IconoLaptop />
            </span>
            <span className="portal__marca-texto">
              <strong>TechAsset</strong>
              <small>INNOVATECH</small>
            </span>
          </Link>

          <nav className="portal__nav" aria-label="Secciones del portal">
            <a href="#funciones">Funciones</a>
            <a href="#como-funciona">Cómo funciona</a>
            <a href="#seguridad">Seguridad</a>
          </nav>

          <div className="portal__acciones">
            <button
              type="button"
              className="boton-icono portal__tema"
              onClick={alternarTema}
              aria-label={tema === "oscuro" ? "Cambiar a tema claro" : "Cambiar a tema oscuro"}
              title={tema === "oscuro" ? "Cambiar a tema claro" : "Cambiar a tema oscuro"}
            >
              {tema === "oscuro" ? <IconoSol /> : <IconoLuna />}
            </button>

            {sesion ? (
              <>
                <span className="portal__sesion" title={sesion.usuario?.correo}>
                  <span aria-hidden="true">{sesion.usuario?.nombreCompleto?.split(" ")[0]}</span>
                  <small>{sesion.usuario?.rol}</small>
                </span>
                <Link to="/panel" className="boton boton--primario boton--pequeno">
                  Ir al panel
                  <IconoFlechaDerecha tamano={16} />
                </Link>
                <button type="button" className="portal__salir" onClick={logout}>
                  Salir
                </button>
              </>
            ) : (
              <Link to="/login" className="boton boton--primario boton--pequeno">
                Iniciar sesión
                <IconoFlechaDerecha tamano={16} />
              </Link>
            )}
          </div>
        </div>
      </header>

      <main id="contenido">
        <section className="portal__hero">
          <div className="portal__contenedor portal__hero-rejilla">
            <div className="portal__hero-texto">
              <span className="portal__sello">
                <IconoEscudo tamano={15} />
                Portal corporativo · Innovatech Solutions
              </span>
              <h1>
                El inventario tecnológico de tu empresa, <span>bajo control</span>.
              </h1>
              <p>
                TechAsset centraliza equipos, préstamos y devoluciones. Consulta la disponibilidad, asigna
                responsables y toma decisiones con reportes actualizados, sin hojas de cálculo dispersas.
              </p>

              <div className="portal__hero-acciones">
                <Link to={sesion ? "/panel" : "/login"} className="boton boton--primario">
                  {sesion ? "Ir al panel de control" : "Acceder al sistema"}
                  <IconoFlechaDerecha tamano={18} />
                </Link>
                <a href="#funciones" className="boton boton--secundario">
                  Conocer las funciones
                </a>
              </div>

              <ul className="portal__beneficios" aria-label="Beneficios principales">
                {BENEFICIOS.map((beneficio) => (
                  <li key={beneficio}>
                    <span aria-hidden="true">
                      <IconoCheck tamano={16} />
                    </span>
                    {beneficio}
                  </li>
                ))}
              </ul>
            </div>

            <div className="portal__vista" aria-label="Vista previa del panel de TechAsset">
              <div className="portal__vista-cabecera">
                <span className="portal__vista-punto portal__vista-punto--rojo" aria-hidden="true" />
                <span className="portal__vista-punto portal__vista-punto--ambar" aria-hidden="true" />
                <span className="portal__vista-punto portal__vista-punto--verde" aria-hidden="true" />
                <span className="portal__vista-url">techasset · panel de control</span>
              </div>

              <div className="portal__vista-cuerpo">
                <div className="portal__vista-titulo">
                  <span>
                    <small>Resumen del inventario</small>
                    <strong>Panel de control</strong>
                  </span>
                  <span className="portal__vista-chip">
                    <IconoBaseDatos tamano={13} />
                    En línea
                  </span>
                </div>

                <div className="portal__vista-indicadores">
                  <div>
                    <small>Equipos</small>
                    <strong>18</strong>
                  </div>
                  <div>
                    <small>Disponibles</small>
                    <strong>8</strong>
                  </div>
                  <div>
                    <small>Prestados</small>
                    <strong>8</strong>
                  </div>
                </div>

                <div className="portal__vista-lista">
                  <div className="portal__vista-fila">
                    <span className="portal__vista-equipo">
                      <IconoLaptop tamano={16} />
                      <span>
                        <strong>Laptop Dell Latitude 5440</strong>
                        <small>TA-0001 · Desarrollo</small>
                      </span>
                    </span>
                    <span className="portal__estado portal__estado--ambar">
                      <IconoReloj tamano={13} /> Prestado
                    </span>
                  </div>
                  <div className="portal__vista-fila">
                    <span className="portal__vista-equipo">
                      <IconoLaptop tamano={16} />
                      <span>
                        <strong>Laptop HP EliteBook 840</strong>
                        <small>TA-0002 · Marketing</small>
                      </span>
                    </span>
                    <span className="portal__estado portal__estado--verde">
                      <IconoCheck tamano={13} /> Disponible
                    </span>
                  </div>
                  <div className="portal__vista-fila">
                    <span className="portal__vista-equipo">
                      <IconoAlerta tamano={16} />
                      <span>
                        <strong>Monitor LG 24"</strong>
                        <small>TA-0007 · Diseño</small>
                      </span>
                    </span>
                    <span className="portal__estado portal__estado--ambar">
                      <IconoReloj tamano={13} /> Prestado
                    </span>
                  </div>
                </div>

                <p className="portal__vista-nota">Vista de demostración · los datos reales requieren sesión</p>
              </div>
            </div>
          </div>
        </section>

        <section id="funciones" className="portal__seccion">
          <div className="portal__contenedor">
            <header className="portal__seccion-cabecera">
              <span className="portal__etiqueta">Funciones</span>
              <h2>Todo el ciclo del equipo en un solo lugar</h2>
              <p>Desde el alta del activo hasta la devolución, con reglas claras y evidencia de cada movimiento.</p>
            </header>

            <div className="portal__rejilla-funciones">
              {FUNCIONES.map(({ Icono, titulo, texto }) => (
                <article key={titulo} className="portal__funcion">
                  <span className="portal__funcion-icono" aria-hidden="true">
                    <Icono />
                  </span>
                  <h3>{titulo}</h3>
                  <p>{texto}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section id="como-funciona" className="portal__seccion portal__seccion--alterna">
          <div className="portal__contenedor">
            <header className="portal__seccion-cabecera">
              <span className="portal__etiqueta">Cómo funciona</span>
              <h2>Tres pasos para dejar atrás las hojas de cálculo</h2>
            </header>

            <div className="portal__pasos">
              {PASOS.map((paso) => (
                <article key={paso.numero} className="portal__paso">
                  <span className="portal__paso-numero" aria-hidden="true">
                    {paso.numero}
                  </span>
                  <h3>{paso.titulo}</h3>
                  <p>{paso.texto}</p>
                </article>
              ))}
            </div>

            <div className="portal__centrado">
              <Link to={sesion ? "/panel" : "/login"} className="boton boton--primario">
                {sesion ? "Abrir mi panel" : "Ingresar con mi cuenta corporativa"}
                <IconoFlechaDerecha tamano={18} />
              </Link>
            </div>
          </div>
        </section>

        <section id="seguridad" className="portal__seguridad">
          <div className="portal__contenedor portal__seguridad-fila">
            <div>
              <span className="portal__etiqueta portal__etiqueta--clara">Seguridad</span>
              <h2>Información de la empresa, solo para su personal</h2>
              <p>
                El acceso es exclusivo para cuentas @innovatech.pe. Cada rol ve únicamente las acciones que le
                corresponden y la API valida el permiso en cada petición, no solo en la pantalla.
              </p>
            </div>
            <ul className="portal__seguridad-lista">
              <li>
                <IconoCheck tamano={18} /> Contraseñas protegidas con BCrypt.
              </li>
              <li>
                <IconoCheck tamano={18} /> Sesiones JWT con expiración y rol.
              </li>
              <li>
                <IconoCheck tamano={18} /> Contraseña temporal en el primer ingreso.
              </li>
              <li>
                <IconoCheck tamano={18} /> Rutas privadas y respuestas 401/403.
              </li>
            </ul>
          </div>
        </section>
      </main>

      <footer className="portal__pie">
        <div className="portal__contenedor portal__pie-fila">
          <div className="portal__pie-marca">
            <span className="portal__logo portal__logo--pequeno" aria-hidden="true">
              <IconoLaptop />
            </span>
            <span>
              <strong>TechAsset</strong>
              <small>Innovatech Solutions S.A.C. · 2026</small>
            </span>
          </div>
          <p>Sistema de gestión de inventario y préstamo de equipos tecnológicos.</p>
          <div className="portal__pie-enlaces">
            <Link to="/login">Acceso corporativo</Link>
            <a href="mailto:soporte@innovatech.pe">soporte@innovatech.pe</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
