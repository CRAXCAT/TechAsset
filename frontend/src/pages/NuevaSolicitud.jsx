import { useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import Boton from "../components/ui/Boton.jsx";
import CampoArea from "../components/ui/CampoArea.jsx";
import CampoSelect from "../components/ui/CampoSelect.jsx";
import CampoTexto from "../components/ui/CampoTexto.jsx";
import EncabezadoPagina from "../components/ui/EncabezadoPagina.jsx";
import EtiquetaEquipo from "../components/ui/EtiquetaEquipo.jsx";
import {
  IconoAlerta,
  IconoCheck,
  IconoFlechaDerecha,
  IconoInfo,
  IconoLaptop,
  IconoLista,
  IconoRefrescar,
} from "../components/ui/Iconos.jsx";
import { useNotificaciones } from "../context/ToastContext.jsx";
import { useCatalogos } from "../hooks/useCatalogos.js";
import { solicitudService } from "../services/solicitudService.js";
import { fechaDeHoyISO, formatearFechaLarga, sumarDiasISO } from "../utils/formato.js";
import { validarSolicitud } from "../utils/validaciones.js";

const VALORES = {
  equipoId: "",
  fechaPrestamo: fechaDeHoyISO(),
  fechaDevolucion: sumarDiasISO(7),
  motivo: "",
};

export default function NuevaSolicitud() {
  const [parametros] = useSearchParams();
  const { equipos, cargando, error } = useCatalogos({ usuarios: false, equipos: true });
  const { notificar } = useNotificaciones();

  const [valores, setValores] = useState({
    ...VALORES,
    equipoId: parametros.get("equipoId") ?? "",
  });
  const [errores, setErrores] = useState({});
  const [errorGeneral, setErrorGeneral] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [creada, setCreada] = useState(null);

  const disponibles = equipos.filter((equipo) => equipo.estado === "Disponible");
  const equipoSeleccionado = equipos.find((equipo) => equipo.id === valores.equipoId);

  const actualizar = (campo) => (evento) => {
    setValores((actuales) => ({ ...actuales, [campo]: evento.target.value }));
    setErrores((actuales) => ({ ...actuales, [campo]: undefined }));
  };

  const registrar = async (evento) => {
    evento.preventDefault();
    setErrorGeneral("");
    const encontrados = validarSolicitud(valores);
    setErrores(encontrados);

    if (Object.keys(encontrados).length > 0) {
      document.getElementById(Object.keys(encontrados)[0])?.focus();
      notificar({
        tipo: "error",
        titulo: "Revise la solicitud",
        mensaje: "Hay datos que deben corregirse antes de enviarla.",
      });
      return;
    }

    setEnviando(true);
    try {
      const solicitud = await solicitudService.crear({
        equipoId: valores.equipoId,
        fechaPrestamo: valores.fechaPrestamo,
        fechaDevolucion: valores.fechaDevolucion,
        motivo: valores.motivo.trim(),
      });
      setCreada(solicitud);
      setValores({ ...VALORES, fechaPrestamo: fechaDeHoyISO(), fechaDevolucion: sumarDiasISO(7) });
      setErrores({});
      notificar({
        tipo: "exito",
        titulo: "Solicitud registrada",
        mensaje: `${solicitud.codigo} · ${solicitud.equipo} quedó pendiente de revisión.`,
      });
    } catch (fallo) {
      setErrorGeneral(fallo.message);
      notificar({ tipo: "error", titulo: "No se pudo registrar la solicitud", mensaje: fallo.message });
    } finally {
      setEnviando(false);
    }
  };

  const limpiar = () => {
    setValores({ ...VALORES, fechaPrestamo: fechaDeHoyISO(), fechaDevolucion: sumarDiasISO(7) });
    setErrores({});
    setErrorGeneral("");
    setCreada(null);
    document.getElementById("equipoId")?.focus();
  };

  return (
    <div className="pagina">
      <EncabezadoPagina
        titulo="Nueva solicitud de equipo"
        descripcion="Solicite un equipo disponible. El Responsable de Tecnología revisará la solicitud y, si la aprueba, se generará el préstamo."
        acciones={
          <Link to="/solicitudes" className="boton boton--secundario">
            <IconoLista tamano={18} />
            <span>Mis solicitudes</span>
          </Link>
        }
      />

      {creada && (
        <div className="confirmacion" role="status">
          <span className="confirmacion__icono" aria-hidden="true">
            <IconoCheck />
          </span>
          <div className="confirmacion__cuerpo">
            <strong>Solicitud {creada.codigo} registrada correctamente.</strong>
            <p>
              {creada.equipo} · {creada.solicitante} · devolución prevista{" "}
              {formatearFechaLarga(creada.fechaDevolucion)}
            </p>
          </div>
          <div className="confirmacion__acciones">
            <Link to="/solicitudes" className="boton boton--secundario boton--pequeno">
              Ver mis solicitudes
              <IconoFlechaDerecha tamano={16} />
            </Link>
          </div>
        </div>
      )}

      <div className="rejilla-formulario">
        <section className="panel" aria-labelledby="titulo-form-solicitud">
          <header className="panel__cabecera">
            <div>
              <h2 id="titulo-form-solicitud" className="panel__titulo">
                Datos de la solicitud
              </h2>
              <p className="panel__subtitulo">
                Los campos marcados con <span className="asterisco">*</span> son obligatorios.
              </p>
            </div>
          </header>

          <form className="panel__cuerpo formulario" onSubmit={registrar} noValidate>
            {errorGeneral && (
              <div className="aviso aviso--error" role="alert">
                <IconoAlerta />
                <div>
                  <strong>La solicitud no se registró.</strong>
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
              id="equipoId"
              etiqueta="Equipo disponible"
              requerido
              placeholder={cargando ? "Cargando equipos..." : "Seleccione el equipo"}
              opciones={disponibles.map((equipo) => ({
                valor: equipo.id,
                etiqueta: `${equipo.codigoPatrimonial} · ${equipo.nombre}`,
              }))}
              ayuda={
                disponibles.length === 0
                  ? "No hay equipos disponibles en este momento."
                  : "Solo aparecen equipos en estado Disponible."
              }
              error={errores.equipoId}
              value={valores.equipoId}
              onChange={actualizar("equipoId")}
            />

            {equipoSeleccionado && (
              <div className="nota">
                <IconoLaptop />
                <p>
                  <strong>{equipoSeleccionado.nombre}</strong> · {equipoSeleccionado.categoria} ·{" "}
                  {equipoSeleccionado.marca}
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
              id="motivo"
              etiqueta="Motivo de la solicitud"
              requerido
              rows={4}
              maxLength={300}
              contador={{ actual: valores.motivo.length, maximo: 300 }}
              placeholder="Ej.: Necesito una laptop para el trabajo remoto durante la semana de despliegue."
              ayuda="El Responsable usará este motivo para evaluar la solicitud."
              error={errores.motivo}
              value={valores.motivo}
              onChange={actualizar("motivo")}
            />

            <div className="formulario__acciones">
              <Boton type="submit" cargando={enviando}>
                {enviando ? "Registrando solicitud..." : "Enviar solicitud"}
              </Boton>
              <Boton variante="secundario" onClick={limpiar} disabled={enviando} icono={<IconoRefrescar tamano={16} />}>
                Limpiar formulario
              </Boton>
              <p className="formulario__nota">
                <IconoInfo tamano={16} />
                La solicitud no reserva el equipo: la disponibilidad se confirma al aprobarla.
              </p>
            </div>
          </form>
        </section>

        <aside className="columna-lateral">
          <section className="panel" aria-labelledby="titulo-disponibles-solicitud">
            <header className="panel__cabecera">
              <div>
                <h2 id="titulo-disponibles-solicitud" className="panel__titulo">
                  <IconoLaptop tamano={18} /> Equipos disponibles
                </h2>
                <p className="panel__subtitulo">{disponibles.length} equipo(s) para solicitar.</p>
              </div>
            </header>
            <div className="panel__cuerpo">
              {disponibles.length === 0 ? (
                <p className="texto-ayuda">No hay equipos disponibles. Consulte el inventario más tarde.</p>
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

          <section className="panel" aria-labelledby="titulo-reglas-solicitud">
            <header className="panel__cabecera">
              <h2 id="titulo-reglas-solicitud" className="panel__titulo">
                Qué se valida
              </h2>
            </header>
            <div className="panel__cuerpo">
              <ul className="lista-reglas">
                <li><span className="lista-reglas__codigo">RN-01</span><span>El equipo no debe tener un préstamo activo.</span></li>
                <li><span className="lista-reglas__codigo">RN-02</span><span>No se solicita un equipo en Mantenimiento.</span></li>
                <li><span className="lista-reglas__codigo">RN-03</span><span>No se solicita un equipo dado de Baja.</span></li>
                <li><span className="lista-reglas__codigo">RN-04</span><span>La devolución debe ser posterior al préstamo.</span></li>
                <li><span className="lista-reglas__codigo">Única</span><span>Solo puede existir una solicitud pendiente por equipo.</span></li>
              </ul>
            </div>
          </section>

          <div className="nota nota--tarjeta">
            <IconoCheck />
            <p>Si el Responsable rechaza la solicitud, el equipo permanece disponible y la observación queda registrada.</p>
          </div>
        </aside>
      </div>
    </div>
  );
}
