export default function Boton({
  variante = "primario",
  cargando = false,
  icono = null,
  className = "",
  children,
  disabled,
  type = "button",
  ...props
}) {
  return (
    <button
      type={type}
      className={`boton boton--${variante} ${className}`}
      disabled={disabled || cargando}
      aria-busy={cargando || undefined}
      {...props}
    >
      {cargando ? (
        <span className="girador" aria-hidden="true" />
      ) : (
        icono && (
          <span className="boton__icono" aria-hidden="true">
            {icono}
          </span>
        )
      )}
      <span>{children}</span>
    </button>
  );
}
