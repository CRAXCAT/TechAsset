import { useEffect, useState } from "react";
import Boton from "../components/ui/Boton.jsx";
import CampoSelect from "../components/ui/CampoSelect.jsx";
import CampoTexto from "../components/ui/CampoTexto.jsx";
import Cargando from "../components/ui/Cargando.jsx";
import EncabezadoPagina from "../components/ui/EncabezadoPagina.jsx";
import EstadoVacio from "../components/ui/EstadoVacio.jsx";
import EtiquetaRol from "../components/ui/EtiquetaRol.jsx";
import {
  IconoAlerta,
  IconoBuscar,
  IconoFiltro,
  IconoNuevo,
  IconoRefrescar,
  IconoUsuarios,
} from "../components/ui/Iconos.jsx";
import Modal from "../components/ui/Modal.jsx";
import TablaDatos from "../components/ui/TablaDatos.jsx";
import { useNotificaciones } from "../context/ToastContext.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { useUsuarios } from "../hooks/useUsuarios.js";
import { usuarioService } from "../services/usuarioService.js";
import { AREAS, ROLES } from "../utils/constantes.js";
import { formatearFecha } from "../utils/formato.js";
import { validarUsuario } from "../utils/validaciones.js";

const VALORES = { nombres: "", apellidos: "", correo: "", area: "Desarrollo", rol: "Colaborador", claveTemporal: "" };
const ORDEN = ["nombres", "apellidos", "correo", "area", "rol", "claveTemporal"];

export default function Usuarios() {
  const { esAdministrador, usuario: sesion } = useAuth();
  const { notificar } = useNotificaciones();

  const [filtros, setFiltros] = useState({ texto: "", area: "", rol: "", activo: "" });
  const [aplicados, setAplicados] = useState({ texto: "", area: "", rol: "", activo: "" });
  const { datos, cargando, error, recargar } = useUsuarios(aplicados);

  const [modal, setModal] = useState(false);
  const [editando, setEditando] = useState(null);
  const [valores, setValores] = useState(VALORES);
  const [errores, setErrores] = useState({});
  const [errorGeneral, setErrorGeneral] = useState("");
  const [guardando, setGuardando] = useState(false);
  const [cambiandoId, setCambiandoId] = useState(null);

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
    setFiltros({ texto: "", area: "", rol: "", activo: "" });
    setAplicados({ texto: "", area: "", rol: "", activo: "" });
  };

  const abrirCrear = () => {
    setEditando(null);
    setValores(VALORES);
    setModal(true);
  };

  const abrirEditar = (usuario) => {
    setEditando(usuario);
    setValores({
      nombres: usuario.nombres,
      apellidos: usuario.apellidos,
      correo: usuario.correo,
      area: usuario.area,
      rol: usuario.rol,
      claveTemporal: "",
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
    const encontrados = validarUsuario(valores, Boolean(editando));
    setErrores(encontrados);

    if (Object.keys(encontrados).length > 0) {
      document.getElementById(ORDEN.find((campo) => encontrados[campo]))?.focus();
      return;
    }

    setGuardando(true);
    try {
      const dto = {
        nombres: valores.nombres.trim(),
        apellidos: valores.apellidos.trim(),
        correo: valores.correo.trim().toLowerCase(),
        area: valores.area,
        rol: valores.rol,
        ...(editando ? {} : { claveTemporal: valores.claveTemporal }),
      };

      if (editando) {
        await usuarioService.actualizar(editando.id, dto);
        notificar({ tipo: "exito", titulo: "Usuario actualizado", mensaje: `${dto.nombres} ${dto.apellidos} se guardó correctamente.` });
      } else {
        const creado = await usuarioService.crear(dto);
        notificar({
          tipo: "exito",
          titulo: "Usuario registrado",
          mensaje: `${creado.nombreCompleto} recibió una contraseña temporal.`,
        });
      }

      setModal(false);
      recargar();
    } catch (fallo) {
      setErrorGeneral(fallo.message);
    } finally {
      setGuardando(false);
    }
  };

  const alternarActivo = async (usuario) => {
    setCambiandoId(usuario.id);
    try {
      const actualizado = await usuarioService.cambiarActivo(usuario.id, !usuario.activo);
      notificar({
        tipo: "exito",
        titulo: actualizado.activo ? "Cuenta habilitada" : "Cuenta deshabilitada",
        mensaje: `${actualizado.nombreCompleto} ahora está ${actualizado.activo ? "activo" : "inactivo"}.`,
      });
      recargar();
    } catch (fallo) {
      notificar({ tipo: "error", titulo: "No se pudo cambiar el estado", mensaje: fallo.message });
    } finally {
      setCambiandoId(null);
    }
  };

  const columnas = [
    {
      clave: "nombre",
      titulo: "Colaborador",
      render: (u) => (
        <span>
          <span className="tabla__titulo">{u.nombreCompleto}</span>
          <span className="tabla__categoria">{u.correo}</span>
        </span>
      ),
    },
    { clave: "area", titulo: "Área" },
    { clave: "rol", titulo: "Rol", render: (u) => <EtiquetaRol rol={u.rol} /> },
    {
      clave: "estado",
      titulo: "Estado",
      render: (u) => (
        <span className={`etiqueta etiqueta--${u.activo ? "verde" : "gris"}`}>
          <span className="etiqueta__punto" aria-hidden="true" />
          {u.activo ? "Activo" : "Inactivo"}
        </span>
      ),
    },
    {
      clave: "registro",
      titulo: "Registro",
      render: (u) => <span className="tabla__fecha">{formatearFecha(u.fechaRegistro?.slice(0, 10))}</span>,
    },
    {
      clave: "acciones",
      titulo: "Acciones",
      render: (u) => (
        <div className="acciones-tabla">
          <button
            type="button"
            className="boton boton--fantasma boton--pequeno"
            onClick={() => abrirEditar(u)}
            disabled={!esAdministrador}
            title={esAdministrador ? "Editar usuario" : "Solo el administrador edita usuarios"}
          >
            Editar
          </button>
          <button
            type="button"
            className="boton boton--fantasma boton--pequeno"
            onClick={() => alternarActivo(u)}
            disabled={!esAdministrador || cambiandoId === u.id || u.id === sesion?.id}
            title={u.id === sesion?.id ? "No puede deshabilitar su propia cuenta" : "Habilitar o deshabilitar"}
          >
            {cambiandoId === u.id ? "Guardando..." : u.activo ? "Deshabilitar" : "Habilitar"}
          </button>
        </div>
      ),
    },
  ];

  return (
    <div className="pagina">
      <EncabezadoPagina
        titulo="Usuarios"
        descripcion="Colaboradores de Innovatech Solutions con su área, rol y estado de acceso."
        acciones={
          <>
            <span className="nota-chip">
              <IconoUsuarios tamano={16} />
              {sesion?.rol}
            </span>
            <Boton
              onClick={abrirCrear}
              icono={<IconoNuevo tamano={18} />}
              disabled={!esAdministrador}
              title={esAdministrador ? "Registrar usuario" : "Solo el administrador registra usuarios"}
            >
              Nuevo usuario
            </Boton>
          </>
        }
      />

      {!esAdministrador && (
        <div className="aviso aviso--advertencia" role="status">
          <IconoUsuarios />
          <p>La cuenta con rol {sesion?.rol} puede consultar el directorio, pero solo el administrador registra o deshabilita usuarios (RN-09).</p>
        </div>
      )}

      <section className="panel panel--filtros" aria-labelledby="titulo-filtros-usuarios">
        <header className="panel__cabecera">
          <div>
            <h2 id="titulo-filtros-usuarios" className="panel__titulo">
              <IconoFiltro tamano={18} /> Buscar y filtrar
            </h2>
            <p className="panel__subtitulo">{datos.length} usuario(s) encontrado(s).</p>
          </div>
        </header>

        <form className="panel__cuerpo barra-filtros barra-filtros--usuarios" onSubmit={buscar} role="search">
          <div className="buscador">
            <label htmlFor="busqueda-usuario" className="campo__etiqueta">
              Buscar
            </label>
            <div className="buscador__control">
              <span className="buscador__icono" aria-hidden="true">
                <IconoBuscar tamano={18} />
              </span>
              <input
                id="busqueda-usuario"
                type="search"
                className="campo__control"
                placeholder="Nombre, apellido o correo"
                value={filtros.texto}
                onChange={(evento) => setFiltros({ ...filtros, texto: evento.target.value })}
              />
            </div>
          </div>

          <CampoSelect
            id="filtro-area"
            etiqueta="Área"
            placeholder="Todas las áreas"
            opciones={AREAS}
            value={filtros.area}
            onChange={(evento) => {
              setFiltros({ ...filtros, area: evento.target.value });
              setAplicados({ ...filtros, area: evento.target.value });
            }}
          />

          <CampoSelect
            id="filtro-rol"
            etiqueta="Rol"
            placeholder="Todos los roles"
            opciones={ROLES.map((r) => r.valor)}
            value={filtros.rol}
            onChange={(evento) => {
              setFiltros({ ...filtros, rol: evento.target.value });
              setAplicados({ ...filtros, rol: evento.target.value });
            }}
          />

          <CampoSelect
            id="filtro-activo"
            etiqueta="Estado"
            placeholder="Todos"
            opciones={[{ valor: "true", etiqueta: "Activos" }, { valor: "false", etiqueta: "Inactivos" }]}
            value={filtros.activo}
            onChange={(evento) => {
              setFiltros({ ...filtros, activo: evento.target.value });
              setAplicados({ ...filtros, activo: evento.target.value });
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

      <section className="panel" aria-labelledby="titulo-directorio">
        <header className="panel__cabecera panel__cabecera--tabla">
          <div>
            <h2 id="titulo-directorio" className="panel__titulo">
              Directorio
            </h2>
            <p className="panel__subtitulo" role="status">
              {cargando ? "Consultando la API..." : `${datos.length} resultado(s)`}
            </p>
          </div>
        </header>

        <div className="panel__cuerpo panel__cuerpo--sin-relleno">
          {cargando && <Cargando filas={5} etiqueta="Cargando usuarios" />}
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
              titulo="No hay usuarios que coincidan"
              mensaje="Cambie los filtros o registre un nuevo colaborador."
              accion={esAdministrador ? <Boton onClick={abrirCrear} icono={<IconoNuevo tamano={18} />}>Nuevo usuario</Boton> : null}
            />
          )}
          {!cargando && !error && datos.length > 0 && (
            <TablaDatos
              columnas={columnas}
              filas={datos}
              claveFila={(u) => u.id}
              tituloOculto="Usuarios registrados en TechAsset"
            />
          )}
        </div>
      </section>

      <Modal
        abierto={modal}
        titulo={editando ? `Editar ${editando.nombreCompleto}` : "Registrar usuario"}
        descripcion="El correo debe pertenecer a @innovatech.pe y es único en el sistema."
        alCerrar={() => !guardando && setModal(false)}
        pie={
          <>
            <Boton variante="secundario" onClick={() => setModal(false)} disabled={guardando}>
              Cancelar
            </Boton>
            <Boton onClick={guardar} cargando={guardando}>
              {guardando ? "Guardando..." : editando ? "Guardar cambios" : "Registrar usuario"}
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
            <CampoTexto id="nombres" etiqueta="Nombres" requerido maxLength={100} error={errores.nombres} value={valores.nombres} onChange={actualizarCampo("nombres")} />
            <CampoTexto id="apellidos" etiqueta="Apellidos" requerido maxLength={100} error={errores.apellidos} value={valores.apellidos} onChange={actualizarCampo("apellidos")} />
          </div>

          <CampoTexto
            id="correo"
            etiqueta="Correo institucional"
            type="email"
            requerido
            placeholder="nombre.apellido@innovatech.pe"
            error={errores.correo}
            ayuda="Dominio corporativo @innovatech.pe."
            value={valores.correo}
            onChange={actualizarCampo("correo")}
          />

          <div className="formulario__fila">
            <CampoSelect id="area" etiqueta="Área" requerido opciones={AREAS} error={errores.area} value={valores.area} onChange={actualizarCampo("area")} />
            <CampoSelect
              id="rol"
              etiqueta="Rol"
              requerido
              opciones={ROLES.map((r) => ({ valor: r.valor, etiqueta: `${r.valor} · ${r.descripcion}` }))}
              error={errores.rol}
              value={valores.rol}
              onChange={actualizarCampo("rol")}
            />
          </div>

          {!editando && (
            <CampoTexto
              id="claveTemporal"
              etiqueta="Contraseña temporal"
              type="password"
              requerido
              autoComplete="new-password"
              ayuda="El colaborador deberá cambiarla en su primer ingreso."
              error={errores.claveTemporal}
              value={valores.claveTemporal}
              onChange={actualizarCampo("claveTemporal")}
            />
          )}
        </form>
      </Modal>
    </div>
  );
}
