import { useState } from "react";
import Boton from "../components/ui/Boton.jsx";
import CampoSelect from "../components/ui/CampoSelect.jsx";
import Cargando from "../components/ui/Cargando.jsx";
import EncabezadoPagina from "../components/ui/EncabezadoPagina.jsx";
import EstadoVacio from "../components/ui/EstadoVacio.jsx";
import {
  IconoAlerta,
  IconoBuscar,
  IconoFiltro,
  IconoRefrescar,
  IconoReloj,
} from "../components/ui/Iconos.jsx";
import Paginacion from "../components/ui/Paginacion.jsx";
import TablaDatos from "../components/ui/TablaDatos.jsx";
import { useMovimientos } from "../hooks/useMovimientos.js";
import { formatearFechaHora } from "../utils/formato.js";

const ENTIDADES = ["Prestamo", "Solicitud", "Equipo", "Usuario"];
const ACCIONES = ["Crear", "Registrar", "Devolver", "Aprobar", "Rechazar", "Actualizar", "Estado", "Eliminar"];

export default function Movimientos() {
  const [filtros, setFiltros] = useState({ texto: "", entidad: "", accion: "" });
  const [aplicados, setAplicados] = useState({ texto: "", entidad: "", accion: "" });
  const [pagina, setPagina] = useState(1);

  const { datos, cargando, error, recargar } = useMovimientos({
    ...aplicados,
    pagina,
    tamanoPagina: 12,
  });

  const movimientos = datos?.items ?? [];
  const total = datos?.total ?? 0;
  const totalPaginas = datos?.totalPaginas ?? 0;
  const desdeRango = total === 0 ? 0 : (pagina - 1) * 12 + 1;
  const hastaRango = Math.min(pagina * 12, total);

  const buscar = (evento) => {
    evento.preventDefault();
    setAplicados({ ...filtros });
    setPagina(1);
  };

  const limpiar = () => {
    setFiltros({ texto: "", entidad: "", accion: "" });
    setAplicados({ texto: "", entidad: "", accion: "" });
    setPagina(1);
  };

  const columnas = [
    {
      clave: "fecha",
      titulo: "Fecha",
      render: (m) => <span className="tabla__fecha">{formatearFechaHora(m.fecha)}</span>,
    },
    {
      clave: "entidad",
      titulo: "Entidad",
      render: (m) => (
        <span>
          <span className="tabla__titulo">{m.entidad}</span>
          <span className="tabla__categoria">{m.entidadId.slice(0, 8)}…</span>
        </span>
      ),
    },
    {
      clave: "accion",
      titulo: "Acción",
      render: (m) => <span className={`etiqueta etiqueta--${m.accion === "Rechazar" ? "rojo" : m.accion === "Aprobar" ? "verde" : "azul"}`}>{m.accion}</span>,
    },
    { clave: "detalle", titulo: "Detalle", render: (m) => <span className="tabla__detalle">{m.detalle}</span> },
    { clave: "usuario", titulo: "Responsable", render: (m) => <span className="tabla__fecha">{m.usuarioNombre || "Sistema"}</span> },
  ];

  return (
    <div className="pagina">
      <EncabezadoPagina
        titulo="Movimientos"
        descripcion="Auditoría de las operaciones registradas: préstamos, devoluciones, solicitudes y revisiones."
        acciones={
          <span className="nota-chip">
            <IconoReloj tamano={16} />
            {total} movimiento(s)
          </span>
        }
      />

      <section className="panel panel--filtros" aria-labelledby="titulo-filtros-movimientos">
        <header className="panel__cabecera">
          <div>
            <h2 id="titulo-filtros-movimientos" className="panel__titulo">
              <IconoFiltro tamano={18} /> Buscar en la auditoría
            </h2>
            <p className="panel__subtitulo">Cada registro conserva la fecha, el actor y el detalle de la operación.</p>
          </div>
        </header>

        <form className="panel__cuerpo barra-filtros barra-filtros--movimientos" onSubmit={buscar} role="search">
          <div className="buscador">
            <label htmlFor="busqueda-movimiento" className="campo__etiqueta">
              Buscar
            </label>
            <div className="buscador__control">
              <span className="buscador__icono" aria-hidden="true">
                <IconoBuscar tamano={18} />
              </span>
              <input
                id="busqueda-movimiento"
                type="search"
                className="campo__control"
                placeholder="Detalle, usuario, entidad o acción"
                value={filtros.texto}
                onChange={(evento) => setFiltros({ ...filtros, texto: evento.target.value })}
              />
            </div>
          </div>

          <CampoSelect
            id="filtro-entidad"
            etiqueta="Entidad"
            placeholder="Todas las entidades"
            opciones={ENTIDADES}
            value={filtros.entidad}
            onChange={(evento) => {
              setFiltros({ ...filtros, entidad: evento.target.value });
              setAplicados({ ...filtros, entidad: evento.target.value });
              setPagina(1);
            }}
          />

          <CampoSelect
            id="filtro-accion"
            etiqueta="Acción"
            placeholder="Todas las acciones"
            opciones={ACCIONES}
            value={filtros.accion}
            onChange={(evento) => {
              setFiltros({ ...filtros, accion: evento.target.value });
              setAplicados({ ...filtros, accion: evento.target.value });
              setPagina(1);
            }}
          />

          <div className="barra-filtros__botones">
            <Boton type="submit" icono={<IconoBuscar tamano={16} />}>
              Buscar
            </Boton>
            <Boton variante="fantasma" onClick={limpiar}>
              Limpiar
            </Boton>
          </div>
        </form>
      </section>

      <section className="panel" aria-labelledby="titulo-lista-movimientos">
        <header className="panel__cabecera panel__cabecera--tabla">
          <div>
            <h2 id="titulo-lista-movimientos" className="panel__titulo">
              Registro de auditoría
            </h2>
            <p className="panel__subtitulo" role="status">
              {cargando ? "Consultando la API..." : `${total} movimiento(s)`}
            </p>
          </div>
        </header>

        <div className="panel__cuerpo panel__cuerpo--sin-relleno">
          {cargando && <Cargando filas={6} etiqueta="Cargando movimientos" />}
          {!cargando && error && (
            <div className="aviso aviso--error aviso--compacto" role="alert">
              <IconoAlerta />
              <p>{error}</p>
              <Boton variante="secundario" onClick={recargar} icono={<IconoRefrescar tamano={16} />}>
                Reintentar
              </Boton>
            </div>
          )}
          {!cargando && !error && movimientos.length === 0 && (
            <EstadoVacio
              titulo="No hay movimientos que coincidan"
              mensaje="Cambie los filtros o realice una operación para generar un nuevo registro."
            />
          )}
          {!cargando && !error && movimientos.length > 0 && (
            <>
              <TablaDatos
                columnas={columnas}
                filas={movimientos}
                claveFila={(m) => m.id}
                tituloOculto="Movimientos de auditoría"
              />
              <Paginacion
                pagina={pagina}
                totalPaginas={totalPaginas}
                total={total}
                desde={desdeRango}
                hasta={hastaRango}
                sustantivo="movimientos"
                alCambiar={setPagina}
              />
            </>
          )}
        </div>
      </section>
    </div>
  );
}
