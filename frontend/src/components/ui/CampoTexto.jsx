import { useId } from "react";
import { IconoAlerta } from "./Iconos.jsx";

/**
 * Campo de texto reutilizable: etiqueta visible, ayuda, contador y error
 * junto al campo. El error se anuncia con role="alert" y aria-describedby.
 */
export default function CampoTexto({
  etiqueta,
  ayuda,
  error,
  requerido = false,
  contador,
  sufijo,
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

      <div className={`campo__control-envoltura ${sufijo ? "campo__control-envoltura--con-sufijo" : ""}`}>
        <input
          id={campoId}
          className="campo__control"
          aria-invalid={error ? "true" : undefined}
          aria-describedby={descrito}
          aria-required={requerido || undefined}
          {...props}
        />
        {sufijo && <span className="campo__sufijo">{sufijo}</span>}
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
