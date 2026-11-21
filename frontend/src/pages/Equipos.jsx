import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Boton from "../components/ui/Boton.jsx";
import CampoSelect from "../components/ui/CampoSelect.jsx";
import CampoTexto from "../components/ui/CampoTexto.jsx";
import Cargando from "../components/ui/Cargando.jsx";
import EncabezadoPagina from "../components/ui/EncabezadoPagina.jsx";
import EstadoVacio from "../components/ui/EstadoVacio.jsx";
import EtiquetaEquipo from "../components/ui/EtiquetaEquipo.jsx";
import {
  IconoAlerta,
  IconoBuscar,
  IconoFiltro,
  IconoInfo,
  IconoLaptop,
  IconoNuevo,
  IconoRefrescar,
} from "../components/ui/Iconos.jsx";
import Modal from "../components/ui/Modal.jsx";
import TablaDatos from "../components/ui/TablaDatos.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { useNotificaciones } from "../context/ToastContext.jsx";
import { useEquipos } from "../hooks/useEquipos.js";
import { equipoService } from "../services/equipoService.js";
import { CATEGORIAS, ESTADOS_EQUIPO } from "../utils/constantes.js";
import { validarEquipo } from "../utils/validaciones.js";

const VALORES = { codigoPatrimonial: "", nombre: "", categoria: "Laptop", marca: "", estado: "Disponible" };

export default function Equipos() {
  const { usuario, esAdministrador } = useAuth();
  const puedeGestionar = esAdministrador || usuario?.rol === "Responsable";
  const { notificar } = useNotificaciones();

  const [filtros, setFiltros] = useState({ texto: "", categoria: "", estado: "" });
  const [aplicados, setAplicados] = useState({ texto: "", categoria: "", estado: "" });
  const { datos, cargando, error, recargar } = useEquipos(aplicados);

  const [modal, setModal] = useState(false);
  const [editando, setEditando] = useState(null);
  const [valores, setValores] = useState(VALORES);
  const [errores, setErrores] = useState({});
  const [errorGeneral, setErrorGeneral] = useState("");
  const [guardando, setGuardando] = useState(false);

  const [estadoModal, setEstadoModal] = useState(null);
  const [nuevoEstado, setNuevoEstado] = useState("Disponible");
  const [errorEstado, setErrorEstado] = useState("");
  const [cambiandoEstado, setCambiandoEstado] = useState(false);

  const [eliminando, setEliminando] = useState(null);
  const [errorEliminar, setErrorEliminar] = useState("");
  const [borrando, setBorrando] = useState(false);

  useEffect(() => {
    setValores(VALORES);
    setErrores({});
    setErrorGeneral("");
  }, [modal]);

  const buscar = (evento) => {
    evento.preventDefault();
    setAplicados({ ...filtros });
  };

  const limpiar = () => {
    setFiltros({ texto: "", categoria: "", estado: "" });
    setAplicados({ texto: "", categoria: "", estado: "" });
  };

  const abrirCrear = () => {
    setEditando(null);
    setValores(VALORES);
    setModal(true);
  };

  const abrirEditar = (equipo) => {
    setEditando(equipo);
    setValores({
      codigoPatrimonial: equipo.codigoPatrimonial,
      nombre: equipo.nombre,
      categoria: equipo.categoria,
      marca: equipo.marca,
      estado: equipo.estado,
    });
    setModal(true);
  };

  const actualizarCampo = (campo) => (evento) => {
    setValores((actuales) => ({ ...actuales, [campo]: evento.target.value }));
    setErrores((actuales) => ({ ...actuales, [campo]: undefined }));
  };

  const guardar = async (evento) => {
    evento.preventDefault();
    setErrorGeneral("");
    const encontrados = validarEquipo(valores);
    setErrores(encontrados);

    if (Object.keys(encontrados).length > 0) {
      document.getElementById(Object.keys(encontrados)[0])?.focus();
      return;
    }

    setGuardando(true);
    try {
      const dto = {
        codigoPatrimonial: valores.codigoPatrimonial.trim(),
        nombre: valores.nombre.trim(),
        categoria: valores.categoria,
        marca: valores.marca.trim(),
        estado: valores.estado,
      };

      if (editando) {
        await equipoService.actualizar(editando.id, dto);
        notificar({ tipo: "exito", titulo: "Equipo actualizado", mensaje: `${dto.nombre} se guardó correctamente.` });
      } else {
        const creado = await equipoService.crear(dto);
        notificar({ tipo: "exito", titulo: "Equipo registrado", mensaje: `${creado.codigoPatrimonial} · ${creado.nombre}.` });
      }

      setModal(false);
      recargar();
    } catch (fallo) {
      setErrorGeneral(fallo.message);
    } finally {
      setGuardando(false);
    }
  };

  const abrirEstado = (equipo) => {
    setNuevoEstado(equipo.estado === "Prestado" ? "Disponible" : equipo.estado);
    setErrorEstado("");
    setEstadoModal(equipo);
  };

  const guardarEstado = async () => {
    setCambiandoEstado(true);
    setErrorEstado("");
    try {
      await equipoService.cambiarEstado(estadoModal.id, nuevoEstado);
      notificar({ tipo: "exito", titulo: "Estado actualizado", mensaje: `${estadoModal.nombre} ahora está en ${nuevoEstado}.` });
      setEstadoModal(null);
      recargar();
    } catch (fallo) {
      setErrorEstado(fallo.message);
    } finally {
      setCambiandoEstado(false);
    }
  };

  const confirmarEliminar = async () => {
    setBorrando(true);
    setErrorEliminar("");
    try {
      await equipoService.eliminar(eliminando.id);
      notificar({ tipo: "exito", titulo: "Equipo eliminado", mensaje: `${eliminando.nombre} se retiró del inventario.` });
      setEliminando(null);
      recargar();
    } catch (fallo) {
      setErrorEliminar(fallo.message);
    } finally {
      setBorrando(false);
    }
  };

  const columnas = [
    { clave: "codigo", titulo: "Código", render: (e) => <span className="tabla__codigo">{e.codigoPatrimonial}</span> },
    {
      clave: "equipo",
      titulo: "Equipo",
      render: (e) => (
        <span>
          <span className="tabla__titulo">{e.nombre}</span>
          <span className="tabla__categoria">{e.categoria}</span>
        </span>
      ),
    },
    { clave: "marca", titulo: "Marca" },
    { clave: "estado", titulo: "Estado", render: (e) => <EtiquetaEquipo estado={e.estado} /> },
    {
      clave: "prestamo",
      titulo: "Préstamo",
      render: (e) => (
        <span className={`etiqueta etiqueta--${e.prestamoActivo ? "ambar" : "gris"}`}>
          {e.prestamoActivo ? "Activo" : `${e.totalPrestamos} histórico(s)`}
        </span>
      ),
    },
    {
      clave: "acciones",
      titulo: "Acciones",
      render: (e) => {
        if (!puedeGestionar) {
          return e.estado === "Disponible" ? (
            <Link
              to={`/solicitudes/nueva?equipoId=${e.id}`}
              className="boton boton--fantasma boton--pequeno"
            >
              Solicitar
            </Link>
          ) : (
            <span className="texto-ayuda">No disponible</span>
          );
        }

        return (
          <div className="acciones-tabla">
            <button type="button" className="boton boton--fantasma boton--pequeno" onClick={() => abrirEditar(e)}>
              Editar
            </button>
            <button
              type="button"
              className="boton boton--fantasma boton--pequeno"
              onClick={() => abrirEstado(e)}
              disabled={e.prestamoActivo}
              title={e.prestamoActivo ? "Registre la devolución antes de cambiar el estado" : "Cambiar estado"}
            >
              Estado
            </button>
            {esAdministrador && (
              <button
                type="button"
                className="boton boton--fantasma boton--pequeno"
                onClick={() => {
                  setErrorEliminar("");
                  setEliminando(e);
                }}
                title={e.totalPrestamos > 0 ? "No se puede eliminar un equipo con historial (RN-06)" : "Eliminar equipo"}
              >
                Eliminar
              </button>
            )}
          </div>
        );
      },
    },
  ];

  return (
    <div className="pagina">
      <EncabezadoPagina
        titulo="Inventario de equipos"
        descripcion="Activos tecnológicos de Innovatech Solutions: disponibilidad, estado y préstamos."
        acciones={
          <>
            <span className="nota-chip">
              <IconoLaptop tamano={16} />
              {datos.length} equipos
            </span>
            {puedeGestionar ? (
              <Boton onClick={abrirCrear} icono={<IconoNuevo tamano={18} />}>
                Nuevo equipo
              </Boton>
            ) : (
              <Link to="/solicitudes/nueva" className="boton boton--primario">
                <IconoNuevo tamano={18} />
                <span>Solicitar equipo</span>
              </Link>
            )}
          </>
        }
      />

      {!puedeGestionar && (
        <div className="aviso aviso--advertencia" role="status">
          <IconoInfo />
          <p>Su rol puede consultar el inventario y solicitar equipos disponibles. La gestión de altas, estados y bajas corresponde al Responsable o al Administrador.</p>
        </div>
      )}

      <section className="panel panel--filtros" aria-labelledby="titulo-filtros-equipos">
        <header className="panel__cabecera">
          <div>
            <h2 id="titulo-filtros-equipos" className="panel__titulo">
              <IconoFiltro tamano={18} /> Buscar en el inventario
            </h2>
            <p className="panel__subtitulo">Filtre por código, nombre, marca, categoría o estado.</p>
          </div>
        </header>

        <form className="panel__cuerpo barra-filtros barra-filtros--equipos" onSubmit={buscar} role="search">
          <div className="buscador">
            <label htmlFor="busqueda-equipo" className="campo__etiqueta">
              Buscar
            </label>
            <div className="buscador__control">
              <span className="buscador__icono" aria-hidden="true">
                <IconoBuscar tamano={18} />
              </span>
              <input
                id="busqueda-equipo"
                type="search"
                className="campo__control"
                placeholder="Código, nombre o marca"
                value={filtros.texto}
                onChange={(evento) => setFiltros({ ...filtros, texto: evento.target.value })}
              />
            </div>
          </div>

          <CampoSelect
            id="filtro-categoria"
            etiqueta="Categoría"
            placeholder="Todas las categorías"
            opciones={CATEGORIAS}
            value={filtros.categoria}
            onChange={(evento) => {
              setFiltros({ ...filtros, categoria: evento.target.value });
              setAplicados({ ...filtros, categoria: evento.target.value });
            }}
          />

          <CampoSelect
            id="filtro-estado-equipo"
            etiqueta="Estado"
            placeholder="Todos los estados"
            opciones={ESTADOS_EQUIPO.map((e) => e.valor)}
            value={filtros.estado}
            onChange={(evento) => {
              setFiltros({ ...filtros, estado: evento.target.value });
              setAplicados({ ...filtros, estado: evento.target.value });
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

      <section className="panel" aria-labelledby="titulo-inventario">
        <header className="panel__cabecera panel__cabecera--tabla">
          <div>
            <h2 id="titulo-inventario" className="panel__titulo">
              Inventario
            </h2>
            <p className="panel__subtitulo" role="status">
              {cargando ? "Consultando la API..." : `${datos.length} resultado(s)`}
            </p>
          </div>
          {puedeGestionar ? (
            <Link to="/prestamos/nuevo" className="enlace">
              Registrar préstamo
            </Link>
          ) : (
            <Link to="/solicitudes/nueva" className="enlace">
              Solicitar equipo
            </Link>
          )}
        </header>

        <div className="panel__cuerpo panel__cuerpo--sin-relleno">
          {cargando && <Cargando filas={6} etiqueta="Cargando equipos" />}
          {!cargando && error && (
            <div className="aviso aviso--error aviso--compacto" role="alert">
              <IconoAlerta />
              <p>{error}</p>
              <Boton variante="secundario" onClick={recargar} icono={<IconoRefrescar tamano={16} />}>
                Reintentar
              </Boton>
            </div>
          )}
          {!cargando && !error && datos.length === 0 && (
            <EstadoVacio
              titulo="No hay equipos que coincidan"
              mensaje="Cambie los filtros o registre un nuevo equipo tecnológico."
              accion={puedeGestionar ? <Boton onClick={abrirCrear} icono={<IconoNuevo tamano={18} />}>Nuevo equipo</Boton> : null}
            />
          )}
          {!cargando && !error && datos.length > 0 && (
            <TablaDatos columnas={columnas} filas={datos} claveFila={(e) => e.id} tituloOculto="Inventario de equipos tecnológicos" />
          )}
        </div>
      </section>

      <Modal
        abierto={modal}
        titulo={editando ? `Editar ${editando.nombre}` : "Registrar equipo"}
        descripcion="El código patrimonial es único (RN-07). El estado Prestado se asigna desde un préstamo."
        alCerrar={() => !guardando && setModal(false)}
        pie={
          <>
            <Boton variante="secundario" onClick={() => setModal(false)} disabled={guardando}>
              Cancelar
            </Boton>
            <Boton onClick={guardar} cargando={guardando}>
              {guardando ? "Guardando..." : editando ? "Guardar cambios" : "Registrar equipo"}
            </Boton>
          </>
        }
      >
        <form className="formulario" onSubmit={guardar} noValidate>
          {errorGeneral && (
            <div className="aviso aviso--error aviso--compacto" role="alert">
              <IconoAlerta />
              <p>{errorGeneral}</p>
            </div>
          )}

          <div className="formulario__fila">
            <CampoTexto
              id="codigoPatrimonial"
              etiqueta="Código patrimonial"
              requerido
              placeholder="EQ-0001"
              maxLength={50}
              error={errores.codigoPatrimonial}
              value={valores.codigoPatrimonial}
              onChange={actualizarCampo("codigoPatrimonial")}
            />
            <CampoTexto
              id="nombre"
              etiqueta="Nombre del equipo"
              requerido
              placeholder="Laptop Dell Latitude 5440"
              maxLength={100}
              error={errores.nombre}
              value={valores.nombre}
              onChange={actualizarCampo("nombre")}
            />
          </div>

          <div className="formulario__fila">
            <CampoSelect
              id="categoria"
              etiqueta="Categoría"
              requerido
              opciones={CATEGORIAS}
              error={errores.categoria}
              value={valores.categoria}
              onChange={actualizarCampo("categoria")}
            />
            <CampoTexto
              id="marca"
              etiqueta="Marca"
              requerido
              placeholder="Dell, HP, Lenovo..."
              maxLength={50}
              error={errores.marca}
              value={valores.marca}
              onChange={actualizarCampo("marca")}
            />
          </div>

          <CampoSelect
            id="estado"
            etiqueta="Estado"
            requerido
            opciones={ESTADOS_EQUIPO.filter((e) => e.valor !== "Prestado").map((e) => e.valor)}
            ayuda="Prestado se asigna automáticamente al registrar un préstamo."
            error={errores.estado}
            value={valores.estado}
            onChange={actualizarCampo("estado")}
          />
        </form>
      </Modal>

      <Modal
        abierto={Boolean(estadoModal)}
        tamano="pequeno"
        titulo="Cambiar estado del equipo"
        alCerrar={() => !cambiandoEstado && setEstadoModal(null)}
        pie={
          <>
            <Boton variante="secundario" onClick={() => setEstadoModal(null)} disabled={cambiandoEstado}>
              Cancelar
            </Boton>
            <Boton onClick={guardarEstado} cargando={cambiandoEstado}>
              Guardar estado
            </Boton>
          </>
        }
      >
        {estadoModal && (
          <div className="confirmar">
            <p>
              <strong>{estadoModal.codigoPatrimonial}</strong> · {estadoModal.nombre}
            </p>
            <CampoSelect
              id="nuevo-estado"
              etiqueta="Nuevo estado"
              opciones={ESTADOS_EQUIPO.filter((e) => e.valor !== "Prestado").map((e) => e.valor)}
              value={nuevoEstado}
              onChange={(evento) => setNuevoEstado(evento.target.value)}
            />
            {errorEstado && (
              <p className="campo__error" role="alert">
                <IconoAlerta tamano={16} />
                <span>{errorEstado}</span>
              </p>
            )}
          </div>
        )}
      </Modal>

      <Modal
        abierto={Boolean(eliminando)}
        tamano="pequeno"
        titulo="Eliminar equipo"
        alCerrar={() => !borrando && setEliminando(null)}
        pie={
          <>
            <Boton variante="secundario" onClick={() => setEliminando(null)} disabled={borrando}>
              Cancelar
            </Boton>
            <Boton variante="peligro" onClick={confirmarEliminar} cargando={borrando}>
              Sí, eliminar
            </Boton>
          </>
        }
      >
        {eliminando && (
          <div className="confirmar">
            <p>
              ¿Confirma eliminar <strong>{eliminando.nombre}</strong> ({eliminando.codigoPatrimonial})?
            </p>
            <p className="confirmar__nota">Si el equipo tiene historial de préstamos, el sistema bloqueará la operación (RN-06).</p>
            {errorEliminar && (
              <p className="campo__error" role="alert">
                <IconoAlerta tamano={16} />
                <span>{errorEliminar}</span>
              </p>
            )}
          </div>
        )}
      </Modal>
    </div>
  );
}
