import { useId } from "react";
import { IconoAlerta } from "./Iconos.jsx";

export default function CampoArea({
  etiqueta,
  ayuda,
  error,
  requerido = false,
  contador,
  id,
  className = "",
  ...props
}) {
  const idGenerado = useId();
  const campoId = id ?? `campo-${idGenerado}`;
  const ayudaId = ayuda ? `${campoId}-ayuda` : undefined;
  const errorId = error ? `${campoId}-error` : undefined;
  const contadorId = contador ? `${campoId}-contador` : undefined;
  const descrito = [ayudaId, errorId, contadorId].filter(Boolean).join(" ") || undefined;

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
        {contador && (
          <span id={contadorId} className={`campo__contador ${contador.actual > contador.maximo ? "campo__contador--excedido" : ""}`}>
            {contador.actual}/{contador.maximo}
          </span>
        )}
      </div>

      <textarea
        id={campoId}
        className="campo__control campo__control--area"
        aria-invalid={error ? "true" : undefined}
        aria-describedby={descrito}
        aria-required={requerido || undefined}
        {...props}
      />

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
