import { useEffect, useId, useRef } from "react";
import { createPortal } from "react-dom";
import { IconoCerrar } from "./Iconos.jsx";

const ENFOCABLES =
  'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])';

/**
 * Diálogo modal accesible: cierra con Escape, con el botón X o con el fondo,
 * encierra el foco mientras está abierto y lo devuelve al control de origen.
 */
export default function Modal({ abierto, titulo, descripcion, alCerrar, children, pie, tamano = "mediano" }) {
  const idTitulo = useId();
  const idDescripcion = useId();
  const refDialogo = useRef(null);
  const refAlCerrar = useRef(alCerrar);
  const refOrigen = useRef(null);

  useEffect(() => {
    refAlCerrar.current = alCerrar;
  }, [alCerrar]);

  useEffect(() => {
    if (!abierto) return undefined;

    refOrigen.current = document.activeElement;
    const overflowPrevio = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    const dialogo = refDialogo.current;
    const primerEnfocable = dialogo?.querySelector("[data-autofocus]") ?? dialogo?.querySelector(ENFOCABLES);
    primerEnfocable?.focus();

    const alPresionarTecla = (evento) => {
      if (evento.key === "Escape") {
        evento.preventDefault();
        refAlCerrar.current();
        return;
      }

      if (evento.key !== "Tab" || !dialogo) return;

      const enfocables = Array.from(dialogo.querySelectorAll(ENFOCABLES)).filter(
        (elemento) => elemento.offsetParent !== null
      );

      if (enfocables.length === 0) {
        evento.preventDefault();
        return;
      }

      const primero = enfocables[0];
      const ultimo = enfocables[enfocables.length - 1];

      if (evento.shiftKey && document.activeElement === primero) {
        evento.preventDefault();
        ultimo.focus();
      } else if (!evento.shiftKey && document.activeElement === ultimo) {
        evento.preventDefault();
        primero.focus();
      }
    };

    document.addEventListener("keydown", alPresionarTecla);

    return () => {
      document.removeEventListener("keydown", alPresionarTecla);
      document.body.style.overflow = overflowPrevio;
      refOrigen.current?.focus?.();
    };
  }, [abierto]);

  if (!abierto) return null;

  return createPortal(
    <div className="modal-fondo" onMouseDown={(evento) => evento.target === evento.currentTarget && alCerrar()}>
      <div
        ref={refDialogo}
        className={`modal modal--${tamano}`}
        role="dialog"
        aria-modal="true"
        aria-labelledby={idTitulo}
        aria-describedby={descripcion ? idDescripcion : undefined}
        tabIndex={-1}
      >
        <header className="modal__cabecera">
          <div>
            <h2 id={idTitulo} className="modal__titulo">
              {titulo}
            </h2>
            {descripcion && (
              <p id={idDescripcion} className="modal__descripcion">
                {descripcion}
              </p>
            )}
          </div>
          <button type="button" className="boton-icono" onClick={alCerrar} aria-label="Cerrar la ventana">
            <IconoCerrar />
          </button>
        </header>

        <div className="modal__cuerpo">{children}</div>

        {pie && <footer className="modal__pie">{pie}</footer>}
      </div>
    </div>,
    document.body
  );
}
