import { useState } from "react";
import { Link } from "react-router-dom";
import Boton from "../components/ui/Boton.jsx";
import CampoArea from "../components/ui/CampoArea.jsx";
import CampoSelect from "../components/ui/CampoSelect.jsx";
import CampoTexto from "../components/ui/CampoTexto.jsx";
import EncabezadoPagina from "../components/ui/EncabezadoPagina.jsx";
import EtiquetaEquipo from "../components/ui/EtiquetaEquipo.jsx";
import {
  IconoAlerta,
  IconoCheck,
  IconoDevolver,
  IconoFlechaDerecha,
  IconoInfo,
  IconoLaptop,
  IconoLista,
  IconoRefrescar,
} from "../components/ui/Iconos.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { useNotificaciones } from "../context/ToastContext.jsx";
import { useCatalogos } from "../hooks/useCatalogos.js";
import { prestamoService } from "../services/prestamoService.js";
import {
  fechaDeHoyISO,
  formatearFechaLarga,
  sumarDiasISO,
} from "../utils/formato.js";
import { validarPrestamo } from "../utils/validaciones.js";

const VALORES = {
  usuarioId: "",
  equipoId: "",
  fechaPrestamo: fechaDeHoyISO(),
  fechaDevolucion: sumarDiasISO(7),
  observacion: "",
};

export default function NuevoPrestamo() {
  const { usuario, esAdministrador } = useAuth();
  const puedeGestionar = esAdministrador || usuario?.rol === "Responsable";
  const { notificar } = useNotificaciones();
  const { usuarios, equipos, cargando, error, recargar: recargarCatalogos } = useCatalogos();

  const [valores, setValores] = useState(VALORES);
  const [errores, setErrores] = useState({});
  const [errorGeneral, setErrorGeneral] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [creado, setCreado] = useState(null);

  const colaboradores = usuarios.filter((u) => u.activo && u.rol === "Colaborador");
  const disponibles = equipos.filter((e) => e.estado === "Disponible");
  const equipoSeleccionado = equipos.find((e) => e.id === valores.equipoId);

  const actualizar = (campo) => (evento) => {
    setValores((actuales) => ({ ...actuales, [campo]: evento.target.value }));
    setErrores((actuales) => ({ ...actuales, [campo]: undefined }));
  };

  const registrar = async (evento) => {
    evento.preventDefault();
    setErrorGeneral("");

    if (!puedeGestionar) {
      setErrorGeneral("Solo el Responsable de Tecnología o el Administrador pueden registrar préstamos (RN-05).");
      return;
    }

    const encontrados = validarPrestamo(valores);
    setErrores(encontrados);

    if (Object.keys(encontrados).length > 0) {
      document.getElementById(Object.keys(encontrados)[0])?.focus();
      notificar({ tipo: "error", titulo: "Revise el formulario", mensaje: "Hay datos que deben corregirse antes de registrar el préstamo." });
      return;
    }

    setEnviando(true);
    try {
      const prestamo = await prestamoService.crear({
        usuarioId: valores.usuarioId,
        equipoId: valores.equipoId,
        fechaPrestamo: valores.fechaPrestamo,
        fechaDevolucion: valores.fechaDevolucion,
        observacion: valores.observacion.trim(),
      });

      setCreado(prestamo);
      setValores({ ...VALORES, usuarioId: valores.usuarioId });
      setErrores({});
      recargarCatalogos();
      notificar({
        tipo: "exito",
        titulo: "Préstamo registrado",
        mensaje: `${prestamo.codigo} · ${prestamo.equipo}.`,
      });
    } catch (fallo) {
      setErrorGeneral(fallo.message);
      notificar({ tipo: "error", titulo: "No se pudo registrar el préstamo", mensaje: fallo.message });
    } finally {
      setEnviando(false);
    }
  };

  const limpiar = () => {
    setValores({ ...VALORES, fechaPrestamo: fechaDeHoyISO(), fechaDevolucion: sumarDiasISO(7) });
    setErrores({});
    setErrorGeneral("");
    setCreado(null);
    document.getElementById("usuarioId")?.focus();
  };

  return (
    <div className="pagina">
      <EncabezadoPagina
        titulo="Nuevo préstamo"
        descripcion="Módulo de entrada. Seleccione el colaborador y un equipo disponible; el sistema valida las reglas antes de guardar."
        acciones={
          <Link to="/prestamos" className="boton boton--secundario">
            <IconoLista tamano={18} />
            <span>Ir a préstamos</span>
          </Link>
        }
      />

      {creado && (
        <div className="confirmacion" role="status">
          <span className="confirmacion__icono" aria-hidden="true">
            <IconoCheck />
          </span>
          <div className="confirmacion__cuerpo">
            <strong>Préstamo {creado.codigo} registrado correctamente.</strong>
            <p>
              {creado.equipo} · {creado.solicitante} · devolución {formatearFechaLarga(creado.fechaDevolucion)}
            </p>
          </div>
          <div className="confirmacion__acciones">
            <Link to="/prestamos" className="boton boton--secundario boton--pequeno">
              Ver historial
              <IconoFlechaDerecha tamano={16} />
            </Link>
          </div>
        </div>
      )}

      {!puedeGestionar && (
        <div className="aviso aviso--advertencia" role="status">
          <IconoAlerta />
          <p>Su rol es {usuario?.rol}. Solo el Responsable de Tecnología o el Administrador registran préstamos (RN-05).</p>
        </div>
      )}

      <div className="rejilla-formulario">
        <section className="panel" aria-labelledby="titulo-form-prestamo">
          <header className="panel__cabecera">
            <div>
              <h2 id="titulo-form-prestamo" className="panel__titulo">
                Datos del préstamo
              </h2>
              <p className="panel__subtitulo">Los campos marcados con <span className="asterisco">*</span> son obligatorios.</p>
            </div>
          </header>

          <form className="panel__cuerpo formulario" onSubmit={registrar} noValidate>
            {errorGeneral && (
              <div className="aviso aviso--error" role="alert">
                <IconoAlerta />
                <div>
                  <strong>La operación no se completó.</strong>
                  <p>{errorGeneral}</p>
                </div>
              </div>
            )}

            {error && (
              <div className="aviso aviso--error aviso--compacto" role="alert">
                <IconoAlerta />
                <p>{error}</p>
              </div>
            )}

            <CampoSelect
              id="usuarioId"
              etiqueta="Colaborador"
              requerido
              placeholder={cargando ? "Cargando colaboradores..." : "Seleccione al colaborador"}
              opciones={colaboradores.map((u) => ({ valor: u.id, etiqueta: `${u.nombreCompleto} · ${u.area}` }))}
              ayuda="Solo se muestran colaboradores activos."
              error={errores.usuarioId}
              value={valores.usuarioId}
              onChange={actualizar("usuarioId")}
            />

            <CampoSelect
              id="equipoId"
              etiqueta="Equipo disponible"
              requerido
              placeholder={cargando ? "Cargando equipos..." : "Seleccione el equipo"}
              opciones={disponibles.map((e) => ({ valor: e.id, etiqueta: `${e.codigoPatrimonial} · ${e.nombre}` }))}
              ayuda={disponibles.length === 0 ? "No hay equipos disponibles en este momento." : "Solo aparecen equipos en estado Disponible."}
              error={errores.equipoId}
              value={valores.equipoId}
              onChange={actualizar("equipoId")}
            />

            {equipoSeleccionado && (
              <div className="nota">
                <IconoLaptop />
                <p>
                  <strong>{equipoSeleccionado.nombre}</strong> · {equipoSeleccionado.categoria} · {equipoSeleccionado.marca}
                  <br />
                  Estado actual: <EtiquetaEquipo estado={equipoSeleccionado.estado} />
                </p>
              </div>
            )}

            <div className="formulario__fila">
              <CampoTexto
                id="fechaPrestamo"
                etiqueta="Fecha de préstamo"
                type="date"
                requerido
                min={fechaDeHoyISO()}
                error={errores.fechaPrestamo}
                value={valores.fechaPrestamo}
                onChange={actualizar("fechaPrestamo")}
              />
              <CampoTexto
                id="fechaDevolucion"
                etiqueta="Fecha de devolución"
                type="date"
                requerido
                min={valores.fechaPrestamo || fechaDeHoyISO()}
                error={errores.fechaDevolucion}
                value={valores.fechaDevolucion}
                onChange={actualizar("fechaDevolucion")}
              />
            </div>

            <CampoArea
              id="observacion"
              etiqueta="Motivo del préstamo"
              requerido
              rows={4}
              maxLength={300}
              contador={{ actual: valores.observacion.length, maximo: 300 }}
              placeholder="Ej.: Uso de laptop para trabajo remoto durante la semana de despliegue."
              ayuda="El préstamo queda asociado al responsable que lo registra (RN-05)."
              error={errores.observacion}
              value={valores.observacion}
              onChange={actualizar("observacion")}
            />

            <div className="formulario__acciones">
              <Boton type="submit" cargando={enviando} disabled={!puedeGestionar}>
                {enviando ? "Registrando préstamo..." : "Registrar préstamo"}
              </Boton>
              <Boton variante="secundario" onClick={limpiar} disabled={enviando} icono={<IconoRefrescar tamano={16} />}>
                Limpiar formulario
              </Boton>
              <p className="formulario__nota">
                <IconoInfo tamano={16} />
                Al registrar, el equipo pasa a <strong>Prestado</strong> y no puede asignarse a otra persona (RN-01).
              </p>
            </div>
          </form>
        </section>

        <aside className="columna-lateral">
          <section className="panel" aria-labelledby="titulo-disponibles">
            <header className="panel__cabecera">
              <div>
                <h2 id="titulo-disponibles" className="panel__titulo">
                  <IconoLaptop tamano={18} /> Equipos disponibles
                </h2>
                <p className="panel__subtitulo">{disponibles.length} equipo(s) listos para préstamo.</p>
              </div>
            </header>
            <div className="panel__cuerpo">
              {disponibles.length === 0 ? (
                <p className="texto-ayuda">No hay equipos disponibles. Revise el inventario o registre una devolución.</p>
              ) : (
                <ul className="lista-reglas">
                  {disponibles.slice(0, 6).map((equipo) => (
                    <li key={equipo.id}>
                      <span className="lista-reglas__codigo">{equipo.codigoPatrimonial}</span>
                      <span>
                        {equipo.nombre} · {equipo.categoria}
                      </span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </section>

          <section className="panel" aria-labelledby="titulo-reglas-prestamo">
            <header className="panel__cabecera">
              <h2 id="titulo-reglas-prestamo" className="panel__titulo">
                Reglas que se validan
              </h2>
            </header>
            <div className="panel__cuerpo">
              <ul className="lista-reglas">
                <li><span className="lista-reglas__codigo">RN-01</span><span>Un equipo solo puede tener un préstamo activo.</span></li>
                <li><span className="lista-reglas__codigo">RN-02</span><span>No se presta un equipo en Mantenimiento.</span></li>
                <li><span className="lista-reglas__codigo">RN-03</span><span>No se presta un equipo dado de Baja.</span></li>
                <li><span className="lista-reglas__codigo">RN-04</span><span>La devolución debe ser posterior al préstamo.</span></li>
                <li><span className="lista-reglas__codigo">RN-05</span><span>Todo préstamo registra un responsable.</span></li>
              </ul>
            </div>
          </section>

          <div className="nota nota--tarjeta">
            <IconoDevolver />
            <p>Al registrar la devolución, el equipo vuelve a <strong>Disponible</strong> y se solicita una observación obligatoria (RN-10).</p>
          </div>
        </aside>
      </div>
    </div>
  );
}
