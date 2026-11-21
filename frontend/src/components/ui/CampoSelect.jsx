import { useId } from "react";
import { IconoAlerta, IconoFlechaAbajo } from "./Iconos.jsx";

export default function CampoSelect({
  etiqueta,
  ayuda,
  error,
  requerido = false,
  opciones,
  placeholder = "Seleccione una opción",
  id,
  className = "",
  ...props
}) {
  const idGenerado = useId();
  const campoId = id ?? `campo-${idGenerado}`;
  const ayudaId = ayuda ? `${campoId}-ayuda` : undefined;
  const errorId = error ? `${campoId}-error` : undefined;
  const descrito = [ayudaId, errorId].filter(Boolean).join(" ") || undefined;

  return (
    <div className={`campo ${error ? "campo--error" : ""} ${className}`}>
      <div className="campo__cabecera">
        <label className="campo__etiqueta" htmlFor={campoId}>
          {etiqueta}
          {requerido && (
            <span className="campo__requerido" aria-hidden="true">
              *
            </span>
          )}
          {requerido && <span className="visualmente-oculto"> (obligatorio)</span>}
        </label>
      </div>

      <div className="campo__select-envoltura">
        <select
          id={campoId}
          className="campo__control campo__control--select"
          aria-invalid={error ? "true" : undefined}
          aria-describedby={descrito}
          aria-required={requerido || undefined}
          {...props}
        >
          <option value="">{placeholder}</option>
          {opciones.map((opcion) => {
            const valor = typeof opcion === "string" ? opcion : opcion.valor;
            const texto = typeof opcion === "string" ? opcion : opcion.etiqueta;
            return (
              <option key={valor} value={valor}>
                {texto}
              </option>
            );
          })}
        </select>
        <span className="campo__select-icono" aria-hidden="true">
          <IconoFlechaAbajo tamano={18} />
        </span>
      </div>

      {ayuda && (
        <p id={ayudaId} className="campo__ayuda">
          {ayuda}
        </p>
      )}

      {error && (
        <p id={errorId} className="campo__error" role="alert">
          <IconoAlerta tamano={16} />
          <span>{error}</span>
        </p>
      )}
    </div>
  );
}
