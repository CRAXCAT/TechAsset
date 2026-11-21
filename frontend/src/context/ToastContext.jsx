import { createContext, useCallback, useContext, useMemo, useState } from "react";
import { IconoAlerta, IconoCheck, IconoCerrar, IconoInfo } from "../components/ui/Iconos.jsx";

const ContextoNotificaciones = createContext(null);

const ICONOS = {
  exito: IconoCheck,
  error: IconoAlerta,
  info: IconoInfo,
};

/**
 * Notificaciones no bloqueantes. La región aria-live anuncia el resultado de
 * cada acción sin mover el foco del usuario (retroalimentación informativa).
 */
export function ProveedorNotificaciones({ children }) {
  const [notificaciones, setNotificaciones] = useState([]);

  const cerrar = useCallback((id) => {
    setNotificaciones((actuales) => actuales.filter((n) => n.id !== id));
  }, []);

  const notificar = useCallback(
    ({ tipo = "info", titulo, mensaje, duracion = 5000 }) => {
      const id = crypto.randomUUID();
      setNotificaciones((actuales) => [...actuales, { id, tipo, titulo, mensaje }]);

      if (duracion > 0) {
        window.setTimeout(() => cerrar(id), duracion);
      }

      return id;
    },
    [cerrar]
  );

  const valor = useMemo(() => ({ notificar, cerrar }), [notificar, cerrar]);

  return (
    <ContextoNotificaciones.Provider value={valor}>
      {children}

      <div className="notificaciones" role="region" aria-label="Notificaciones del sistema">
        <div aria-live="polite" aria-atomic="false">
          {notificaciones.map(({ id, tipo, titulo, mensaje }) => {
            const Icono = ICONOS[tipo] ?? IconoInfo;
            return (
              <div key={id} className={`notificacion notificacion--${tipo}`}>
                <span className="notificacion__icono" aria-hidden="true">
                  <Icono />
                </span>
                <div className="notificacion__cuerpo">
                  <p className="notificacion__titulo">{titulo}</p>
                  {mensaje && <p className="notificacion__mensaje">{mensaje}</p>}
                </div>
                <button
                  type="button"
                  className="notificacion__cerrar"
                  onClick={() => cerrar(id)}
                  aria-label={`Cerrar la notificación: ${titulo}`}
                >
                  <IconoCerrar tamano={16} />
                </button>
              </div>
            );
          })}
        </div>
      </div>
    </ContextoNotificaciones.Provider>
  );
}

export function useNotificaciones() {
  const contexto = useContext(ContextoNotificaciones);
  if (!contexto) {
    throw new Error("useNotificaciones debe usarse dentro de ProveedorNotificaciones");
  }
  return contexto;
}
