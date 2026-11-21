import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import Boton from "../components/ui/Boton.jsx";
import CampoArea from "../components/ui/CampoArea.jsx";
import CampoSelect from "../components/ui/CampoSelect.jsx";
import CampoTexto from "../components/ui/CampoTexto.jsx";
import Cargando from "../components/ui/Cargando.jsx";
import EncabezadoPagina from "../components/ui/EncabezadoPagina.jsx";
import EstadoVacio from "../components/ui/EstadoVacio.jsx";
import EtiquetaPrestamo from "../components/ui/EtiquetaPrestamo.jsx";
import {
  IconoAlerta,
  IconoBuscar,
  IconoDevolver,
  IconoFiltro,
  IconoFlechaDerecha,
  IconoInfo,
  IconoNuevo,
  IconoRefrescar,
} from "../components/ui/Iconos.jsx";
import Modal from "../components/ui/Modal.jsx";
import Paginacion from "../components/ui/Paginacion.jsx";
import TablaDatos from "../components/ui/TablaDatos.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { useNotificaciones } from "../context/ToastContext.jsx";
import { useCatalogos } from "../hooks/useCatalogos.js";
import { usePrestamos } from "../hooks/usePrestamos.js";
import { prestamoService } from "../services/prestamoService.js";
import { AREAS, ESTADOS_PRESTAMO, TAMANO_PAGINA } from "../utils/constantes.js";
import { formatearFecha, formatearFechaLarga } from "../utils/formato.js";
import { validarDevolucion } from "../utils/validaciones.js";

export default function Prestamos() {
  const [parametros, setParametros] = useSearchParams();
  const { usuario, esAdministrador } = useAuth();
  const puedeGestionar = esAdministrador || usuario?.rol === "Responsable";
  const { notificar } = useNotificaciones();
  const { equipos } = useCatalogos({ usuarios: false, equipos: true });

  const texto = parametros.get("texto") ?? "";
  const estado = parametros.get("estado") ?? "";
  const area = parametros.get("area") ?? "";
  const equipoId = parametros.get("equipoId") ?? "";
  const desde = parametros.get("desde") ?? "";
  const hasta = parametros.get("hasta") ?? "";
  const pagina = Math.max(1, Number(parametros.get("pagina")) || 1);

  const [busqueda, setBusqueda] = useState(texto);
  const [seleccionado, setSeleccionado] = useState(null);
  const [devolucion, setDevolucion] = useState(null);
  const [observacion, setObservacion] = useState("");
  const [errorDevolucion, setErrorDevolucion] = useState("");
  const [procesando, setProcesando] = useState(false);

  const { datos, cargando, error, recargar } = usePrestamos({
    texto,
    estado,
    area,
    equipoId,
    desde,
    hasta,
    pagina,
    tamanoPagina: TAMANO_PAGINA,
  });

  useEffect(() => {
    setBusqueda(texto);
  }, [texto]);

  const aplicar = (cambios) => {
    const siguientes = new URLSearchParams(parametros);
    Object.entries(cambios).forEach(([clave, valor]) => {
      if (valor) siguientes.set(clave, String(valor));
      else siguientes.delete(clave);
    });
    if (!("pagina" in cambios)) siguientes.set("pagina", "1");
    setParametros(siguientes, { replace: true });
  };

  const buscar = (evento) => {
    evento.preventDefault();
    aplicar({ texto: busqueda.trim() });
  };

  const limpiar = () => {
    setBusqueda("");
    setParametros({}, { replace: true });
  };

  const prestamos = datos?.items ?? [];
  const total = datos?.total ?? 0;
  const totalPaginas = datos?.totalPaginas ?? 0;
  const desdeRango = total === 0 ? 0 : (pagina - 1) * TAMANO_PAGINA + 1;
  const hastaRango = Math.min(pagina * TAMANO_PAGINA, total);
  const filtrosActivos = [texto, estado, area, equipoId, desde, hasta].filter(Boolean).length;

  const abrirDevolucion = (prestamo) => {
    setObservacion("");
    setErrorDevolucion("");
    setDevolucion(prestamo);
  };

  const confirmarDevolucion = async () => {
    const errorTexto = validarDevolucion(observacion);
    if (errorTexto) {
      setErrorDevolucion(errorTexto);
      return;
    }

    setProcesando(true);
    setErrorDevolucion("");
    try {
      const actualizado = await prestamoService.devolver(devolucion.id, observacion.trim());
      notificar({
        tipo: "exito",
        titulo: "Devolución registrada",
        mensaje: `${actualizado.codigo} · ${actualizado.equipo} quedó disponible.`,
      });
      setDevolucion(null);
      setSeleccionado(actualizado);
      recargar();
    } catch (fallo) {
      setErrorDevolucion(fallo.message);
    } finally {
      setProcesando(false);
    }
  };

  const columnas = [
    { clave: "codigo", titulo: "Código", render: (p) => <span className="tabla__codigo">{p.codigo}</span> },
    {
      clave: "equipo",
      titulo: "Equipo",
      render: (p) => (
        <span>
          <span className="tabla__titulo">{p.equipo}</span>
          <span className="tabla__categoria">
            {p.codigoPatrimonial} · {p.categoria}
          </span>
        </span>
      ),
    },
    {
      clave: "solicitante",
      titulo: "Colaborador",
      render: (p) => (
        <span>
          <span className="tabla__titulo">{p.solicitante}</span>
          <span className="tabla__categoria">{p.area}</span>
        </span>
      ),
    },
    { clave: "fechaPrestamo", titulo: "Préstamo", render: (p) => <span className="tabla__fecha">{formatearFecha(p.fechaPrestamo)}</span> },
    {
      clave: "fechaDevolucion",
      titulo: "Devolución",
      render: (p) => (
        <span className="tabla__fecha">
          {formatearFecha(p.fechaDevolucion)}
          {p.fechaDevolucionReal && <span className="tabla__categoria">Real: {formatearFecha(p.fechaDevolucionReal)}</span>}
        </span>
      ),
    },
    { clave: "estado", titulo: "Estado", render: (p) => <EtiquetaPrestamo estado={p.estado} /> },
    {
      clave: "acciones",
      titulo: "Acciones",
      render: (p) => (
        <div className="acciones-tabla">
          <button type="button" className="boton boton--fantasma boton--pequeno" onClick={() => setSeleccionado(p)}>
            Ver
          </button>
          {p.estado === "Activo" && puedeGestionar && (
            <button type="button" className="boton boton--fantasma boton--pequeno" onClick={() => abrirDevolucion(p)}>
              Devolver
            </button>
          )}
        </div>
      ),
    },
  ];

  return (
    <div className="pagina">
      <EncabezadoPagina
        titulo={puedeGestionar ? "Préstamos" : "Mi historial"}
        descripcion={
          puedeGestionar
            ? "Historial y préstamos activos de equipos tecnológicos, con búsqueda y filtros."
            : "Consulte únicamente sus préstamos y el estado de cada devolución."
        }
        acciones={
          <>
            <span className="nota-chip">
              <IconoDevolver tamano={16} />
              {total} registros
            </span>
            {puedeGestionar ? (
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

      <section className="panel panel--filtros" aria-labelledby="titulo-filtros-prestamos">
        <header className="panel__cabecera">
          <div>
            <h2 id="titulo-filtros-prestamos" className="panel__titulo">
              <IconoFiltro tamano={18} /> Buscar y filtrar
            </h2>
            <p className="panel__subtitulo">
              {puedeGestionar
                ? filtrosActivos === 0
                  ? "Sin filtros activos: se muestra el historial completo."
                  : `${filtrosActivos} filtro(s) activo(s). Los criterios se conservan en la dirección.`
                : "Solo se muestran los préstamos asociados a su cuenta."}
            </p>
          </div>
        </header>

        <form className="panel__cuerpo barra-filtros barra-filtros--prestamos" onSubmit={buscar} role="search">
          <div className="buscador">
            <label htmlFor="busqueda-prestamo" className="campo__etiqueta">
              Buscar
            </label>
            <div className="buscador__control">
              <span className="buscador__icono" aria-hidden="true">
                <IconoBuscar tamano={18} />
              </span>
              <input
                id="busqueda-prestamo"
                type="search"
                className="campo__control"
                placeholder="Equipo, código o colaborador"
                value={busqueda}
                onChange={(evento) => setBusqueda(evento.target.value)}
              />
            </div>
          </div>

          <CampoSelect
            id="filtro-estado-prestamo"
            etiqueta="Estado"
            placeholder="Todos los estados"
            opciones={ESTADOS_PRESTAMO.map((e) => e.valor)}
            value={estado}
            onChange={(evento) => aplicar({ estado: evento.target.value })}
          />

          <CampoSelect
            id="filtro-area-prestamo"
            etiqueta="Área"
            placeholder="Todas las áreas"
            opciones={AREAS}
            value={area}
            onChange={(evento) => aplicar({ area: evento.target.value })}
          />

          <CampoSelect
            id="filtro-equipo"
            etiqueta="Equipo"
            placeholder="Todos los equipos"
            opciones={equipos.map((e) => ({ valor: e.id, etiqueta: `${e.codigoPatrimonial} · ${e.nombre}` }))}
            value={equipoId}
            onChange={(evento) => aplicar({ equipoId: evento.target.value })}
          />

          <CampoTexto id="filtro-desde" etiqueta="Desde" type="date" value={desde} onChange={(evento) => aplicar({ desde: evento.target.value })} />
          <CampoTexto id="filtro-hasta" etiqueta="Hasta" type="date" value={hasta} onChange={(evento) => aplicar({ hasta: evento.target.value })} />

          <div className="barra-filtros__botones">
            <Boton type="submit" icono={<IconoBuscar tamano={16} />}>
              Buscar
            </Boton>
            <Boton variante="fantasma" onClick={limpiar} disabled={filtrosActivos === 0 && !busqueda}>
              Limpiar
            </Boton>
          </div>
        </form>
      </section>

      <section className="panel" aria-labelledby="titulo-resultados-prestamos">
        <header className="panel__cabecera panel__cabecera--tabla">
          <div>
            <h2 id="titulo-resultados-prestamos" className="panel__titulo">
              Resultados
            </h2>
            <p className="panel__subtitulo" role="status">
              {cargando ? "Consultando la API..." : `${total} préstamo(s) encontrado(s)`}
            </p>
          </div>
        </header>

        <div className="panel__cuerpo panel__cuerpo--sin-relleno">
          {cargando && <Cargando filas={6} etiqueta="Cargando préstamos" />}
          {!cargando && error && (
            <div className="aviso aviso--error aviso--compacto" role="alert">
              <IconoAlerta />
              <p>{error}</p>
              <Boton variante="secundario" onClick={recargar} icono={<IconoRefrescar tamano={16} />}>
                Reintentar
              </Boton>
            </div>
          )}
          {!cargando && !error && prestamos.length === 0 && (
            <EstadoVacio
              titulo={filtrosActivos > 0 ? "Ningún préstamo coincide" : "Todavía no hay préstamos"}
              mensaje={filtrosActivos > 0 ? "Retire filtros o cambie el criterio de búsqueda." : "Registre el primer préstamo para verlo aquí."}
              accion={
                filtrosActivos > 0 ? (
                  <Boton variante="secundario" onClick={limpiar}>
                    Limpiar filtros
                  </Boton>
                ) : puedeGestionar ? (
                  <Link to="/prestamos/nuevo" className="boton boton--primario">
                    <IconoNuevo tamano={18} />
                    <span>Nuevo préstamo</span>
                  </Link>
                ) : null
              }
            />
          )}
          {!cargando && !error && prestamos.length > 0 && (
            <>
              <TablaDatos columnas={columnas} filas={prestamos} claveFila={(p) => p.id} tituloOculto="Préstamos registrados" />
              <Paginacion
                pagina={pagina}
                totalPaginas={totalPaginas}
                total={total}
                desde={desdeRango}
                hasta={hastaRango}
                sustantivo="préstamos"
                alCambiar={(nueva) => aplicar({ pagina: nueva })}
              />
            </>
          )}
        </div>
      </section>

      <Modal
        abierto={Boolean(seleccionado) && !devolucion}
        titulo={seleccionado ? `Préstamo ${seleccionado.codigo}` : "Detalle"}
        descripcion={seleccionado ? `${seleccionado.equipo} · ${seleccionado.codigoPatrimonial}` : ""}
        alCerrar={() => setSeleccionado(null)}
        pie={
          <>
            <Boton variante="secundario" onClick={() => setSeleccionado(null)}>
              Cerrar
            </Boton>
            {seleccionado?.estado === "Activo" && puedeGestionar && (
              <Boton onClick={() => abrirDevolucion(seleccionado)} icono={<IconoDevolver tamano={16} />}>
                Registrar devolución
              </Boton>
            )}
          </>
        }
      >
        {seleccionado && (
          <div className="detalle">
            <dl className="detalle__datos">
              <div><dt>Colaborador</dt><dd>{seleccionado.solicitante}</dd></div>
              <div><dt>Área</dt><dd>{seleccionado.area}</dd></div>
              <div><dt>Equipo</dt><dd>{seleccionado.equipo}</dd></div>
              <div><dt>Código patrimonial</dt><dd>{seleccionado.codigoPatrimonial}</dd></div>
              <div><dt>Fecha de préstamo</dt><dd>{formatearFechaLarga(seleccionado.fechaPrestamo)}</dd></div>
              <div><dt>Devolución prevista</dt><dd>{formatearFechaLarga(seleccionado.fechaDevolucion)}</dd></div>
              <div><dt>Devolución real</dt><dd>{seleccionado.fechaDevolucionReal ? formatearFechaLarga(seleccionado.fechaDevolucionReal) : "Pendiente"}</dd></div>
              <div><dt>Estado</dt><dd><EtiquetaPrestamo estado={seleccionado.estado} /></dd></div>
              <div><dt>Responsable</dt><dd>{seleccionado.responsable}</dd></div>
              <div><dt>Registrado</dt><dd>{formatearFecha(seleccionado.fechaRegistro?.slice(0, 10))}</dd></div>
            </dl>

            <section className="detalle__descripcion">
              <h3>Motivo del préstamo</h3>
              <p>{seleccionado.observacion}</p>
            </section>

            {seleccionado.observacionDevolucion && (
              <section className="detalle__descripcion">
                <h3>Observación de devolución</h3>
                <p>{seleccionado.observacionDevolucion}</p>
              </section>
            )}

            {seleccionado.estado === "Activo" && (
              <p className="detalle__ayuda">
                <IconoInfo tamano={16} />
                Mientras el préstamo esté activo, el equipo permanece en estado Prestado y no puede asignarse a otra persona (RN-01).
              </p>
            )}
          </div>
        )}
      </Modal>

      <Modal
        abierto={Boolean(devolucion)}
        tamano="pequeno"
        titulo="Registrar devolución"
        descripcion={devolucion ? `${devolucion.equipo} · ${devolucion.solicitante}` : ""}
        alCerrar={() => !procesando && setDevolucion(null)}
        pie={
          <>
            <Boton variante="secundario" onClick={() => setDevolucion(null)} disabled={procesando}>
              Cancelar
            </Boton>
            <Boton onClick={confirmarDevolucion} cargando={procesando}>
              {procesando ? "Registrando..." : "Confirmar devolución"}
            </Boton>
          </>
        }
      >
        {devolucion && (
          <div className="confirmar">
            <p>
              El equipo volverá al estado <strong>Disponible</strong> y el préstamo quedará como <strong>Devuelto</strong>.
            </p>
            <CampoArea
              id="observacion-devolucion"
              etiqueta="Observaciones de la devolución"
              requerido
              rows={4}
              maxLength={300}
              placeholder="Ej.: Equipo devuelto completo, con cargador y funda; sin daños visibles."
              contador={{ actual: observacion.length, maximo: 300 }}
              value={observacion}
              onChange={(evento) => setObservacion(evento.target.value)}
              error={errorDevolucion}
            />
            <p className="confirmar__nota">Toda devolución debe registrar observaciones (RN-10).</p>
          </div>
        )}
      </Modal>

      <p className="pista-teclado">
        <IconoFlechaDerecha tamano={16} />
        Los filtros se guardan en la URL: puede compartir o recuperar la búsqueda.
      </p>
    </div>
  );
}
