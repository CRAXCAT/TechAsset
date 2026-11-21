import { useState } from "react";
import { Link } from "react-router-dom";
import Boton from "../components/ui/Boton.jsx";
import CampoArea from "../components/ui/CampoArea.jsx";
import CampoSelect from "../components/ui/CampoSelect.jsx";
import Cargando from "../components/ui/Cargando.jsx";
import EncabezadoPagina from "../components/ui/EncabezadoPagina.jsx";
import EstadoVacio from "../components/ui/EstadoVacio.jsx";
import EtiquetaSolicitud from "../components/ui/EtiquetaSolicitud.jsx";
import {
  IconoAlerta,
  IconoBuscar,
  IconoCheck,
  IconoDevolver,
  IconoFiltro,
  IconoFlechaDerecha,
  IconoInfo,
  IconoLista,
  IconoNuevo,
  IconoRefrescar,
} from "../components/ui/Iconos.jsx";
import Modal from "../components/ui/Modal.jsx";
import Paginacion from "../components/ui/Paginacion.jsx";
import TablaDatos from "../components/ui/TablaDatos.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { useNotificaciones } from "../context/ToastContext.jsx";
import { useSolicitudes } from "../hooks/useSolicitudes.js";
import { solicitudService } from "../services/solicitudService.js";
import { AREAS, ESTADOS_SOLICITUD, TAMANO_PAGINA } from "../utils/constantes.js";
import { formatearFecha, formatearFechaLarga } from "../utils/formato.js";

export default function Solicitudes() {
  const { usuario, esAdministrador } = useAuth();
  const esGestor = esAdministrador || usuario?.rol === "Responsable";
  const { notificar } = useNotificaciones();

  const [filtros, setFiltros] = useState({ texto: "", estado: "", area: "" });
  const [aplicados, setAplicados] = useState({ texto: "", estado: "", area: "" });
  const [pagina, setPagina] = useState(1);

  const { datos, cargando, error, recargar } = useSolicitudes({
    ...aplicados,
    pagina,
    tamanoPagina: TAMANO_PAGINA,
  });

  const [seleccionada, setSeleccionada] = useState(null);
  const [revision, setRevision] = useState(null);
  const [observacion, setObservacion] = useState("");
  const [errorRevision, setErrorRevision] = useState("");
  const [procesando, setProcesando] = useState(false);

  const solicitudes = datos?.items ?? [];
  const total = datos?.total ?? 0;
  const totalPaginas = datos?.totalPaginas ?? 0;
  const desdeRango = total === 0 ? 0 : (pagina - 1) * TAMANO_PAGINA + 1;
  const hastaRango = Math.min(pagina * TAMANO_PAGINA, total);

  const buscar = (evento) => {
    evento.preventDefault();
    setAplicados({ ...filtros });
    setPagina(1);
  };

  const limpiar = () => {
    setFiltros({ texto: "", estado: "", area: "" });
    setAplicados({ texto: "", estado: "", area: "" });
    setPagina(1);
  };

  const abrirRevision = (solicitud, tipo) => {
    setObservacion("");
    setErrorRevision("");
    setRevision({ solicitud, tipo });
  };

  const confirmarRevision = async () => {
    if (revision.tipo === "Rechazar" && observacion.trim().length < 5) {
      setErrorRevision("Indique el motivo del rechazo (mínimo 5 caracteres).");
      return;
    }

    setProcesando(true);
    setErrorRevision("");
    try {
      const actualizada =
        revision.tipo === "Aprobar"
          ? await solicitudService.aprobar(revision.solicitud.id, observacion.trim())
          : await solicitudService.rechazar(revision.solicitud.id, observacion.trim());

      notificar({
        tipo: "exito",
        titulo: revision.tipo === "Aprobar" ? "Solicitud aprobada" : "Solicitud rechazada",
        mensaje:
          revision.tipo === "Aprobar"
            ? `${actualizada.codigo} generó el préstamo ${actualizada.codigoPrestamo}.`
            : `${actualizada.codigo} quedó rechazada y el equipo sigue disponible.`,
      });
      setRevision(null);
      setSeleccionada(actualizada);
      recargar();
    } catch (fallo) {
      setErrorRevision(fallo.message);
    } finally {
      setProcesando(false);
    }
  };

  const columnas = [
    { clave: "codigo", titulo: "Código", render: (s) => <span className="tabla__codigo">{s.codigo}</span> },
    {
      clave: "equipo",
      titulo: "Equipo",
      render: (s) => (
        <span>
          <span className="tabla__titulo">{s.equipo}</span>
          <span className="tabla__categoria">{s.codigoPatrimonial} · {s.categoria}</span>
        </span>
      ),
    },
    ...(esGestor
      ? [
          {
            clave: "solicitante",
            titulo: "Solicitante",
            render: (s) => (
              <span>
                <span className="tabla__titulo">{s.solicitante}</span>
                <span className="tabla__categoria">{s.area}</span>
              </span>
            ),
          },
        ]
      : []),
    {
      clave: "fechas",
      titulo: "Fechas",
      render: (s) => (
        <span className="tabla__fecha">
          {formatearFecha(s.fechaPrestamo)}
          <span className="tabla__categoria">a {formatearFecha(s.fechaDevolucion)}</span>
        </span>
      ),
    },
    { clave: "estado", titulo: "Estado", render: (s) => <EtiquetaSolicitud estado={s.estado} /> },
    {
      clave: "acciones",
      titulo: "Acciones",
      render: (s) => (
        <div className="acciones-tabla">
          <button type="button" className="boton boton--fantasma boton--pequeno" onClick={() => setSeleccionada(s)}>
            Ver
          </button>
          {esGestor && s.estado === "Pendiente" && (
            <button
              type="button"
              className="boton boton--fantasma boton--pequeno"
              onClick={() => abrirRevision(s, "Aprobar")}
            >
              Revisar
            </button>
          )}
        </div>
      ),
    },
  ];

  return (
    <div className="pagina">
      <EncabezadoPagina
        titulo={esGestor ? "Solicitudes" : "Mis solicitudes"}
        descripcion={
          esGestor
            ? "Revise las solicitudes pendientes, apruébelas para generar el préstamo o recházalas con una observación."
            : "Consulte el estado de sus solicitudes y registre una nueva cuando necesite un equipo."
        }
        acciones={
          <>
            <span className="nota-chip">
              <IconoLista tamano={16} />
              {total} solicitud(es)
            </span>
            {!esGestor && (
              <Link to="/solicitudes/nueva" className="boton boton--primario">
                <IconoNuevo tamano={18} />
                <span>Nueva solicitud</span>
              </Link>
            )}
          </>
        }
      />

      {esGestor && (
        <div className="aviso aviso--advertencia" role="status">
          <IconoInfo />
          <p>
            Al aprobar, el sistema crea el préstamo y marca el equipo como Prestado dentro de una transacción.
            Si algo falla, no se guarda ningún cambio parcial.
          </p>
        </div>
      )}

      <section className="panel panel--filtros" aria-labelledby="titulo-filtros-solicitudes">
        <header className="panel__cabecera">
          <div>
            <h2 id="titulo-filtros-solicitudes" className="panel__titulo">
              <IconoFiltro tamano={18} /> Buscar y filtrar
            </h2>
            <p className="panel__subtitulo">
              {esGestor
                ? "Las solicitudes pendientes aparecen primero."
                : "Solo se muestran sus propias solicitudes."}
            </p>
          </div>
        </header>

        <form className="panel__cuerpo barra-filtros barra-filtros--solicitudes" onSubmit={buscar} role="search">
          <div className="buscador">
            <label htmlFor="busqueda-solicitud" className="campo__etiqueta">
              Buscar
            </label>
            <div className="buscador__control">
              <span className="buscador__icono" aria-hidden="true">
                <IconoBuscar tamano={18} />
              </span>
              <input
                id="busqueda-solicitud"
                type="search"
                className="campo__control"
                placeholder="Equipo, código, solicitante o motivo"
                value={filtros.texto}
                onChange={(evento) => setFiltros({ ...filtros, texto: evento.target.value })}
              />
            </div>
          </div>

          <CampoSelect
            id="filtro-estado-solicitud"
            etiqueta="Estado"
            placeholder="Todos los estados"
            opciones={ESTADOS_SOLICITUD.map((estado) => estado.valor)}
            value={filtros.estado}
            onChange={(evento) => {
              setFiltros({ ...filtros, estado: evento.target.value });
              setAplicados({ ...filtros, estado: evento.target.value });
              setPagina(1);
            }}
          />

          {esGestor && (
            <CampoSelect
              id="filtro-area-solicitud"
              etiqueta="Área"
              placeholder="Todas las áreas"
              opciones={AREAS}
              value={filtros.area}
              onChange={(evento) => {
                setFiltros({ ...filtros, area: evento.target.value });
                setAplicados({ ...filtros, area: evento.target.value });
                setPagina(1);
              }}
            />
          )}

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

      <section className="panel" aria-labelledby="titulo-lista-solicitudes">
        <header className="panel__cabecera panel__cabecera--tabla">
          <div>
            <h2 id="titulo-lista-solicitudes" className="panel__titulo">
              Resultados
            </h2>
            <p className="panel__subtitulo" role="status">
              {cargando ? "Consultando la API..." : `${total} solicitud(es) encontrada(s)`}
            </p>
          </div>
        </header>

        <div className="panel__cuerpo panel__cuerpo--sin-relleno">
          {cargando && <Cargando filas={5} etiqueta="Cargando solicitudes" />}
          {!cargando && error && (
            <div className="aviso aviso--error aviso--compacto" role="alert">
              <IconoAlerta />
              <p>{error}</p>
              <Boton variante="secundario" onClick={recargar} icono={<IconoRefrescar tamano={16} />}>
                Reintentar
              </Boton>
            </div>
          )}
          {!cargando && !error && solicitudes.length === 0 && (
            <EstadoVacio
              titulo="No hay solicitudes que coincidan"
              mensaje={
                esGestor
                  ? "Cambie los filtros para revisar otras solicitudes."
                  : "Registre una nueva solicitud o cambie el filtro de estado."
              }
              accion={
                !esGestor ? (
                  <Link to="/solicitudes/nueva" className="boton boton--primario">
                    <IconoNuevo tamano={18} />
                    <span>Nueva solicitud</span>
                  </Link>
                ) : null
              }
            />
          )}
          {!cargando && !error && solicitudes.length > 0 && (
            <>
              <TablaDatos
                columnas={columnas}
                filas={solicitudes}
                claveFila={(s) => s.id}
                tituloOculto="Solicitudes de equipos tecnológicos"
              />
              <Paginacion
                pagina={pagina}
                totalPaginas={totalPaginas}
                total={total}
                desde={desdeRango}
                hasta={hastaRango}
                sustantivo="solicitudes"
                alCambiar={setPagina}
              />
            </>
          )}
        </div>
      </section>

      <Modal
        abierto={Boolean(seleccionada) && !revision}
        titulo={seleccionada ? `Solicitud ${seleccionada.codigo}` : "Solicitud"}
        descripcion={seleccionada ? `${seleccionada.equipo} · ${seleccionada.codigoPatrimonial}` : ""}
        alCerrar={() => setSeleccionada(null)}
        pie={
          <>
            <Boton variante="secundario" onClick={() => setSeleccionada(null)}>
              Cerrar
            </Boton>
            {esGestor && seleccionada?.estado === "Pendiente" && (
              <>
                <Boton variante="peligro" onClick={() => abrirRevision(seleccionada, "Rechazar")}>
                  Rechazar
                </Boton>
                <Boton onClick={() => abrirRevision(seleccionada, "Aprobar")} icono={<IconoCheck tamano={16} />}>
                  Aprobar
                </Boton>
              </>
            )}
          </>
        }
      >
        {seleccionada && (
          <div className="detalle">
            <dl className="detalle__datos">
              <div><dt>Solicitante</dt><dd>{seleccionada.solicitante}</dd></div>
              <div><dt>Área</dt><dd>{seleccionada.area}</dd></div>
              <div><dt>Equipo</dt><dd>{seleccionada.equipo}</dd></div>
              <div><dt>Estado</dt><dd><EtiquetaSolicitud estado={seleccionada.estado} /></dd></div>
              <div><dt>Fecha de préstamo</dt><dd>{formatearFechaLarga(seleccionada.fechaPrestamo)}</dd></div>
              <div><dt>Devolución prevista</dt><dd>{formatearFechaLarga(seleccionada.fechaDevolucion)}</dd></div>
              <div><dt>Registrada</dt><dd>{formatearFecha(seleccionada.fechaRegistro?.slice(0, 10))}</dd></div>
              {seleccionada.prestamoId && (
                <div><dt>Préstamo generado</dt><dd>{seleccionada.codigoPrestamo}</dd></div>
              )}
              {seleccionada.revisor && (
                <div><dt>Revisada por</dt><dd>{seleccionada.revisor}</dd></div>
              )}
            </dl>

            <section className="detalle__descripcion">
              <h3>Motivo de la solicitud</h3>
              <p>{seleccionada.motivo}</p>
            </section>

            {seleccionada.observacionRevision && (
              <section className="detalle__descripcion">
                <h3>Observación de la revisión</h3>
                <p>{seleccionada.observacionRevision}</p>
              </section>
            )}

            {seleccionada.estado === "Pendiente" && (
              <p className="detalle__ayuda">
                <IconoInfo tamano={16} />
                La solicitud no reserva el equipo. Al aprobar se vuelve a verificar la disponibilidad y se crea el préstamo.
              </p>
            )}
          </div>
        )}
      </Modal>

      <Modal
        abierto={Boolean(revision)}
        tamano="pequeno"
        titulo={revision?.tipo === "Aprobar" ? "Aprobar solicitud" : "Rechazar solicitud"}
        descripcion={
          revision
            ? `${revision.solicitud.codigo} · ${revision.solicitud.equipo} · ${revision.solicitud.solicitante}`
            : ""
        }
        alCerrar={() => !procesando && setRevision(null)}
        pie={
          <>
            <Boton variante="secundario" onClick={() => setRevision(null)} disabled={procesando}>
              Cancelar
            </Boton>
            <Boton
              variante={revision?.tipo === "Rechazar" ? "peligro" : "primario"}
              onClick={confirmarRevision}
              cargando={procesando}
            >
              {procesando
                ? "Procesando..."
                : revision?.tipo === "Aprobar"
                  ? "Aprobar y generar préstamo"
                  : "Confirmar rechazo"}
            </Boton>
          </>
        }
      >
        {revision && (
          <div className="confirmar">
            {revision.tipo === "Aprobar" ? (
              <p>
                Se creará un préstamo para <strong>{revision.solicitud.solicitante}</strong> y el equipo pasará a{" "}
                <strong>Prestado</strong>. La operación se ejecuta en una transacción.
              </p>
            ) : (
              <p>
                El equipo <strong>{revision.solicitud.equipo}</strong> seguirá disponible y la solicitud quedará como{" "}
                <strong>Rechazada</strong>.
              </p>
            )}

            <CampoArea
              id="observacion-revision"
              etiqueta={revision.tipo === "Aprobar" ? "Observación (opcional)" : "Motivo del rechazo"}
              requerido={revision.tipo === "Rechazar"}
              rows={4}
              maxLength={300}
              contador={{ actual: observacion.length, maximo: 300 }}
              placeholder={
                revision.tipo === "Aprobar"
                  ? "Ej.: Aprobado; el colaborador recogerá el equipo en Soporte."
                  : "Ej.: El equipo se reserva para una actividad prioritaria del área."
              }
              ayuda={
                revision.tipo === "Aprobar"
                  ? "Puede dejar una indicación para el colaborador."
                  : "La observación es obligatoria y quedará visible en el historial."
              }
              value={observacion}
              onChange={(evento) => {
                setObservacion(evento.target.value);
                setErrorRevision("");
              }}
              error={errorRevision}
            />

            <p className="confirmar__nota">
              <IconoDevolver tamano={15} /> La aprobación no duplica el préstamo: queda vinculada a la solicitud.
            </p>
          </div>
        )}
      </Modal>

      <p className="pista-teclado">
        <IconoFlechaDerecha tamano={16} />
        {esGestor
          ? "Apruebe solo después de verificar la disponibilidad y las fechas."
          : "Puede consultar el estado de cada solicitud en cualquier momento."}
      </p>
    </div>
  );
}
