import { Link } from "react-router-dom";
import BarrasDatos from "../components/ui/BarrasDatos.jsx";
import Boton from "../components/ui/Boton.jsx";
import Cargando from "../components/ui/Cargando.jsx";
import EncabezadoPagina from "../components/ui/EncabezadoPagina.jsx";
import EtiquetaPrestamo from "../components/ui/EtiquetaPrestamo.jsx";
import {
  IconoAlerta,
  IconoCheck,
  IconoDevolver,
  IconoFlechaDerecha,
  IconoGrafico,
  IconoLaptop,
  IconoLista,
  IconoNuevo,
  IconoRefrescar,
  IconoReloj,
  IconoUsuarios,
} from "../components/ui/Iconos.jsx";
import TarjetaIndicador from "../components/ui/TarjetaIndicador.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { usePrestamos } from "../hooks/usePrestamos.js";
import { useResumen } from "../hooks/useResumen.js";
import { formatearFecha, pluralizar } from "../utils/formato.js";

export default function Dashboard() {
  const { usuario, esAdministrador } = useAuth();
  const rol = usuario?.rol ?? "";
  const puedePrestar = esAdministrador || rol === "Responsable";

  const { resumen, cargando: cargandoResumen, error: errorResumen, recargar: recargarResumen } = useResumen();
  const {
    datos,
    cargando: cargandoPrestamos,
    error: errorPrestamos,
    recargar: recargarPrestamos,
  } = usePrestamos({
    texto: "",
    estado: "Activo",
    area: "",
    equipoId: "",
    desde: "",
    hasta: "",
    pagina: 1,
    tamanoPagina: 5,
  });

  const activos = datos?.items ?? [];

  return (
    <div className="pagina">
      <EncabezadoPagina
        titulo="Panel de control"
        descripcion={`Inventario y préstamos de equipos tecnológicos. Sesión iniciada como: ${rol}.`}
        acciones={
          <>
            {puedePrestar && (
              <Link to="/reportes" className="boton boton--secundario">
                <IconoGrafico tamano={18} />
                <span>Reportes</span>
              </Link>
            )}
            {puedePrestar ? (
              <Link to="/prestamos/nuevo" className="boton boton--primario">
                <IconoNuevo tamano={18} />
                <span>Nuevo préstamo</span>
              </Link>
            ) : (
              <Link to="/solicitudes/nueva" className="boton boton--primario">
                <IconoNuevo tamano={18} />
                <span>Solicitar equipo</span>
              </Link>
            )}
          </>
        }
      />

      {errorResumen && (
        <div className="aviso aviso--error" role="alert">
          <IconoAlerta />
          <div>
            <strong>No se pudieron cargar los indicadores.</strong>
            <p>{errorResumen}</p>
          </div>
          <Boton variante="secundario" onClick={recargarResumen} icono={<IconoRefrescar tamano={16} />}>
            Reintentar
          </Boton>
        </div>
      )}

      {resumen && resumen.solicitudesPendientes > 0 && (
        <div className="aviso aviso--advertencia" role="status">
          <IconoAlerta />
          <div>
            <strong>
              {pluralizar(resumen.solicitudesPendientes, "solicitud pendiente", "solicitudes pendientes")} de revisión.
            </strong>
            <p>
              {puedePrestar
                ? "Revise las solicitudes, verifique la disponibilidad y apruebe o rechace con una observación."
                : "El Responsable de Tecnología revisará su solicitud y le confirmará el resultado."}
            </p>
          </div>
          <Link to="/solicitudes" className="boton boton--secundario boton--pequeno">
            Revisar
            <IconoFlechaDerecha tamano={16} />
          </Link>
        </div>
      )}

      <section className="rejilla-indicadores" aria-label="Indicadores de equipos">
        <TarjetaIndicador etiqueta="Total de equipos" valor={resumen?.totalEquipos ?? 0} detalle="Registrados en PostgreSQL" tono="azul" Icono={IconoLaptop} cargando={cargandoResumen} />
        <TarjetaIndicador etiqueta="Disponibles" valor={resumen?.disponibles ?? 0} detalle="Listos para préstamo" tono="verde" Icono={IconoCheck} cargando={cargandoResumen} />
        <TarjetaIndicador etiqueta="Prestados" valor={resumen?.prestados ?? 0} detalle="Asignados actualmente" tono="azul" Icono={IconoReloj} cargando={cargandoResumen} />
        <TarjetaIndicador etiqueta="Mantenimiento" valor={resumen?.mantenimiento ?? 0} detalle="Fuera de servicio" tono="ambar" Icono={IconoAlerta} cargando={cargandoResumen} />
        <TarjetaIndicador etiqueta="Total de préstamos" valor={resumen?.totalPrestamos ?? 0} detalle={pluralizar(resumen?.prestamosActivos ?? 0, "activo", "activos")} tono="azul" Icono={IconoDevolver} cargando={cargandoResumen} />
      </section>

      <section className="panel panel--destacado" aria-labelledby="titulo-area">
        <div className="panel__cuerpo panel__cuerpo--horizontal">
          <span className="destacado__icono" aria-hidden="true">
            <IconoUsuarios tamano={26} />
          </span>
          <div className="destacado__texto">
            <h2 id="titulo-area" className="panel__titulo">
              {puedePrestar ? "Área con mayor uso" : "Mi área con mayor uso"}
            </h2>
            <p className="panel__subtitulo">
              {puedePrestar
                ? "Calculado con el total de préstamos registrados por área."
                : "Calculado con sus propios préstamos registrados."}
            </p>
          </div>
          {cargandoResumen ? (
            <span className="esqueleto__bloque esqueleto__bloque--numero" aria-hidden="true" />
          ) : (
            <div className="destacado__valor">
              <strong>{resumen?.areaMayorUso ?? "Sin datos"}</strong>
              <span>{pluralizar(resumen?.prestamosAreaMayor ?? 0, "préstamo registrado", "préstamos registrados")}</span>
            </div>
          )}
        </div>
      </section>

      {(resumen?.prestamosActivos ?? 0) > 0 && (
        <div className="aviso aviso--advertencia" role="status">
          <IconoAlerta />
          <div>
            <strong>
              {resumen.prestamosActivos === 1
                ? "1 préstamo activo pendiente de devolución."
                : `${resumen.prestamosActivos} préstamos activos pendientes de devolución.`}
            </strong>
            <p>Revise el historial, registre las devoluciones y mantenga el inventario actualizado.</p>
          </div>
          <Link to="/prestamos?estado=Activo" className="boton boton--secundario boton--pequeno">
            Revisar
            <IconoFlechaDerecha tamano={16} />
          </Link>
        </div>
      )}

      <div className="rejilla-dos-columnas">
        <section className="panel" aria-labelledby="titulo-estados">
          <header className="panel__cabecera">
            <div>
              <h2 id="titulo-estados" className="panel__titulo">
                Equipos por estado
              </h2>
              <p className="panel__subtitulo">Distribución actual del inventario tecnológico.</p>
            </div>
          </header>
          <div className="panel__cuerpo">
            {cargandoResumen ? <Cargando filas={4} /> : <BarrasDatos datos={resumen?.equiposPorEstado} />}
          </div>
        </section>

        <section className="panel" aria-labelledby="titulo-areas">
          <header className="panel__cabecera">
            <div>
              <h2 id="titulo-areas" className="panel__titulo">
                Préstamos por área
              </h2>
              <p className="panel__subtitulo">Áreas que más solicitan equipos.</p>
            </div>
          </header>
          <div className="panel__cuerpo">
            {cargandoResumen ? <Cargando filas={4} /> : <BarrasDatos datos={resumen?.prestamosPorArea} />}
          </div>
        </section>
      </div>

      <div className="rejilla-dos-columnas">
        <section className="panel" aria-labelledby="titulo-mas-usados">
          <header className="panel__cabecera">
            <div>
              <h2 id="titulo-mas-usados" className="panel__titulo">
                Equipos más utilizados
              </h2>
              <p className="panel__subtitulo">Ranking por cantidad de préstamos históricos.</p>
            </div>
          </header>
          <div className="panel__cuerpo">
            {cargandoResumen ? <Cargando filas={4} /> : <BarrasDatos datos={resumen?.equiposMasUtilizados} />}
          </div>
        </section>

        <section className="panel" aria-labelledby="titulo-activos">
          <header className="panel__cabecera">
            <div>
              <h2 id="titulo-activos" className="panel__titulo">
                {puedePrestar ? "Préstamos activos" : "Mis préstamos activos"}
              </h2>
              <p className="panel__subtitulo">Equipos pendientes de devolución.</p>
            </div>
            <Link to="/prestamos?estado=Activo" className="enlace">
              Ver todos
              <IconoFlechaDerecha tamano={16} />
            </Link>
          </header>

          <div className="panel__cuerpo panel__cuerpo--sin-relleno">
            {cargandoPrestamos && <Cargando filas={3} />}
            {!cargandoPrestamos && errorPrestamos && (
              <div className="aviso aviso--error aviso--compacto" role="alert">
                <IconoAlerta />
                <p>{errorPrestamos}</p>
                <Boton variante="secundario" onClick={recargarPrestamos}>
                  Reintentar
                </Boton>
              </div>
            )}
            {!cargandoPrestamos && !errorPrestamos && activos.length === 0 && (
              <div className="vacio-compacto">
                <IconoLaptop tamano={22} />
                <p>No hay préstamos activos.</p>
              </div>
            )}
            {!cargandoPrestamos && !errorPrestamos && activos.length > 0 && (
              <ul className="lista-reciente">
                {activos.map((prestamo) => (
                  <li key={prestamo.id} className="lista-reciente__item">
                    <span className="lista-reciente__codigo">{prestamo.codigo}</span>
                    <span className="lista-reciente__datos">
                      <strong>{prestamo.equipo}</strong>
                      <small>
                        {prestamo.solicitante} · {prestamo.area} · devolución {formatearFecha(prestamo.fechaDevolucion)}
                      </small>
                    </span>
                    <EtiquetaPrestamo estado={prestamo.estado} />
                  </li>
                ))}
              </ul>
            )}
          </div>
        </section>
      </div>

      <section className="panel" aria-labelledby="titulo-accesos">
        <header className="panel__cabecera">
          <h2 id="titulo-accesos" className="panel__titulo">
            Accesos rápidos
          </h2>
        </header>
        <div className="panel__cuerpo rejilla-accesos">
          <Link to="/equipos" className="acceso">
            <span className="acceso__icono" aria-hidden="true">
              <IconoLaptop />
            </span>
            <span className="acceso__texto">
              <strong>Inventario de equipos</strong>
              <p>Consulte disponibilidad, estado y equipos más utilizados.</p>
            </span>
            <IconoFlechaDerecha tamano={18} />
          </Link>

          <Link to="/prestamos" className="acceso">
            <span className="acceso__icono" aria-hidden="true">
              <IconoLista />
            </span>
            <span className="acceso__texto">
              <strong>Historial de préstamos</strong>
              <p>Filtre por estado, área, equipo o rango de fechas.</p>
            </span>
            <IconoFlechaDerecha tamano={18} />
          </Link>
        </div>
      </section>
    </div>
  );
}
