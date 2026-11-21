import { Link } from "react-router-dom";
import BarrasDatos from "../components/ui/BarrasDatos.jsx";
import Boton from "../components/ui/Boton.jsx";
import Cargando from "../components/ui/Cargando.jsx";
import EncabezadoPagina from "../components/ui/EncabezadoPagina.jsx";
import EtiquetaEquipo from "../components/ui/EtiquetaEquipo.jsx";
import {
  IconoAlerta,
  IconoBuscar,
  IconoDescargar,
  IconoFlechaDerecha,
  IconoGrafico,
  IconoLaptop,
  IconoRefrescar,
  IconoTicket,
} from "../components/ui/Iconos.jsx";
import TablaDatos from "../components/ui/TablaDatos.jsx";
import TarjetaIndicador from "../components/ui/TarjetaIndicador.jsx";
import { useNotificaciones } from "../context/ToastContext.jsx";
import { useEquipos } from "../hooks/useEquipos.js";
import { useResumen } from "../hooks/useResumen.js";
import { reporteService } from "../services/reporteService.js";

export default function Reportes() {
  const { notificar } = useNotificaciones();
  const { resumen, cargando, error, recargar } = useResumen();
  const disponibles = useEquipos({ texto: "", categoria: "", estado: "Disponible" });
  const prestados = useEquipos({ texto: "", categoria: "", estado: "Prestado" });

  const descargar = async (tipo) => {
    try {
      const blob =
        tipo === "prestamos"
          ? await reporteService.descargarPrestamos()
          : await reporteService.descargarEquipos();
      const url = URL.createObjectURL(blob);
      const enlace = document.createElement("a");
      enlace.href = url;
      enlace.download = tipo === "prestamos" ? "prestamos-techasset.csv" : "inventario-techasset.csv";
      document.body.appendChild(enlace);
      enlace.click();
      enlace.remove();
      URL.revokeObjectURL(url);
      notificar({ tipo: "exito", titulo: "Reporte generado", mensaje: "El archivo CSV se descargó correctamente." });
    } catch (fallo) {
      notificar({ tipo: "error", titulo: "No se pudo exportar", mensaje: fallo.message });
    }
  };

  const columnasEquipos = [
    { clave: "codigo", titulo: "Código", render: (e) => <span className="tabla__codigo">{e.codigoPatrimonial}</span> },
    {
      clave: "equipo",
      titulo: "Equipo",
      render: (e) => (
        <span>
          <span className="tabla__titulo">{e.nombre}</span>
          <span className="tabla__categoria">{e.categoria} · {e.marca}</span>
        </span>
      ),
    },
    { clave: "estado", titulo: "Estado", render: (e) => <EtiquetaEquipo estado={e.estado} /> },
  ];

  return (
    <div className="pagina">
      <EncabezadoPagina
        titulo="Reportes"
        descripcion="Indicadores, disponibilidad, equipos más utilizados y préstamos por área."
        acciones={
          <>
            <Boton variante="secundario" onClick={() => descargar("equipos")} icono={<IconoDescargar tamano={16} />}>
              Inventario CSV
            </Boton>
            <Boton onClick={() => descargar("prestamos")} icono={<IconoDescargar tamano={16} />}>
              Préstamos CSV
            </Boton>
          </>
        }
      />

      {error && (
        <div className="aviso aviso--error" role="alert">
          <IconoAlerta />
          <p>{error}</p>
          <Boton variante="secundario" onClick={recargar} icono={<IconoRefrescar tamano={16} />}>
            Reintentar
          </Boton>
        </div>
      )}

      <section className="rejilla-indicadores" aria-label="Resumen del inventario">
        <TarjetaIndicador etiqueta="Total de equipos" valor={resumen?.totalEquipos ?? 0} detalle="Inventario registrado" tono="azul" Icono={IconoLaptop} cargando={cargando} />
        <TarjetaIndicador etiqueta="Disponibles" valor={resumen?.disponibles ?? 0} detalle="Listos para préstamo" tono="verde" Icono={IconoBuscar} cargando={cargando} />
        <TarjetaIndicador etiqueta="Prestados" valor={resumen?.prestados ?? 0} detalle="Asignados actualmente" tono="azul" Icono={IconoLaptop} cargando={cargando} />
        <TarjetaIndicador etiqueta="Total de préstamos" valor={resumen?.totalPrestamos ?? 0} detalle={`${resumen?.prestamosActivos ?? 0} activos`} tono="ambar" Icono={IconoGrafico} cargando={cargando} />
        <TarjetaIndicador etiqueta="Solicitudes pendientes" valor={resumen?.solicitudesPendientes ?? 0} detalle={`${resumen?.solicitudesAprobadas ?? 0} aprobadas`} tono="ambar" Icono={IconoTicket} cargando={cargando} />
      </section>

      <div className="rejilla-dos-columnas">
        <section className="panel" aria-labelledby="reporte-estados">
          <header className="panel__cabecera">
            <div>
              <h2 id="reporte-estados" className="panel__titulo">Equipos por estado</h2>
              <p className="panel__subtitulo">Disponibilidad operativa del inventario.</p>
            </div>
          </header>
          <div className="panel__cuerpo">
            {cargando ? <Cargando filas={4} /> : <BarrasDatos datos={resumen?.equiposPorEstado} />}
          </div>
        </section>

        <section className="panel" aria-labelledby="reporte-areas">
          <header className="panel__cabecera">
            <div>
              <h2 id="reporte-areas" className="panel__titulo">Préstamos por área</h2>
              <p className="panel__subtitulo">Área con mayor uso: {resumen?.areaMayorUso ?? "Sin datos"}.</p>
            </div>
          </header>
          <div className="panel__cuerpo">
            {cargando ? <Cargando filas={4} /> : <BarrasDatos datos={resumen?.prestamosPorArea} />}
          </div>
        </section>
      </div>

      <section className="panel" aria-labelledby="reporte-usados">
        <header className="panel__cabecera">
          <div>
            <h2 id="reporte-usados" className="panel__titulo">Equipos más utilizados</h2>
            <p className="panel__subtitulo">Ranking histórico por cantidad de préstamos.</p>
          </div>
        </header>
        <div className="panel__cuerpo">
          {cargando ? <Cargando filas={4} /> : <BarrasDatos datos={resumen?.equiposMasUtilizados} />}
        </div>
      </section>

      <div className="rejilla-dos-columnas">
        <section className="panel" aria-labelledby="reporte-disponibles">
          <header className="panel__cabecera">
            <div>
              <h2 id="reporte-disponibles" className="panel__titulo">Equipos disponibles</h2>
              <p className="panel__subtitulo">{disponibles.datos.length} equipos listos para asignación.</p>
            </div>
            <Link to="/equipos?estado=Disponible" className="enlace">Ver inventario <IconoFlechaDerecha tamano={16} /></Link>
          </header>
          <div className="panel__cuerpo panel__cuerpo--sin-relleno">
            {disponibles.cargando && <Cargando filas={4} />}
            {!disponibles.cargando && disponibles.datos.length > 0 && (
              <TablaDatos columnas={columnasEquipos} filas={disponibles.datos.slice(0, 6)} claveFila={(e) => e.id} tituloOculto="Equipos disponibles" />
            )}
          </div>
        </section>

        <section className="panel" aria-labelledby="reporte-prestados">
          <header className="panel__cabecera">
            <div>
              <h2 id="reporte-prestados" className="panel__titulo">Equipos prestados</h2>
              <p className="panel__subtitulo">{prestados.datos.length} equipos asignados actualmente.</p>
            </div>
            <Link to="/prestamos?estado=Activo" className="enlace">Ver préstamos <IconoFlechaDerecha tamano={16} /></Link>
          </header>
          <div className="panel__cuerpo panel__cuerpo--sin-relleno">
            {prestados.cargando && <Cargando filas={4} />}
            {!prestados.cargando && prestados.datos.length > 0 && (
              <TablaDatos columnas={columnasEquipos} filas={prestados.datos.slice(0, 6)} claveFila={(e) => e.id} tituloOculto="Equipos prestados" />
            )}
          </div>
        </section>
      </div>
    </div>
  );
}
