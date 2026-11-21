import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Boton from "../components/ui/Boton.jsx";
import CampoTexto from "../components/ui/CampoTexto.jsx";
import { IconoAlerta, IconoCandado, IconoCheck, IconoLaptop } from "../components/ui/Iconos.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { useNotificaciones } from "../context/ToastContext.jsx";
import { authService } from "../services/authService.js";
import { esClaveSegura } from "../utils/validaciones.js";

const REGLAS = [
  "Mínimo 8 caracteres.",
  "Al menos una letra mayúscula y una minúscula.",
  "Al menos un número.",
  "Al menos un símbolo (por ejemplo * o #).",
];

export default function CambiarClave() {
  const { usuario, actualizarUsuario, debeCambiarClave, logout } = useAuth();
  const { notificar } = useNotificaciones();
  const navegar = useNavigate();

  const [valores, setValores] = useState({ actual: "", nueva: "", confirmar: "" });
  const [errores, setErrores] = useState({});
  const [errorGeneral, setErrorGeneral] = useState("");
  const [enviando, setEnviando] = useState(false);

  const actualizar = (campo) => (evento) => {
    setValores((actuales) => ({ ...actuales, [campo]: evento.target.value }));
    setErrores((actuales) => ({ ...actuales, [campo]: undefined }));
  };

  const validar = () => {
    const encontrados = {};
    if (!valores.actual) encontrados.actual = "Ingrese su contraseña actual.";
    if (!valores.nueva) {
      encontrados.nueva = "Ingrese la nueva contraseña.";
    } else if (!esClaveSegura(valores.nueva)) {
      encontrados.nueva = "La contraseña debe cumplir las cuatro reglas indicadas.";
    } else if (valores.nueva === valores.actual) {
      encontrados.nueva = "La nueva contraseña debe ser diferente de la actual.";
    }
    if (valores.confirmar !== valores.nueva) {
      encontrados.confirmar = "La confirmación no coincide con la nueva contraseña.";
    }
    return encontrados;
  };

  const guardar = async (evento) => {
    evento.preventDefault();
    setErrorGeneral("");
    const encontrados = validar();
    setErrores(encontrados);

    if (Object.keys(encontrados).length > 0) {
      document.getElementById(Object.keys(encontrados)[0])?.focus();
      return;
    }

    setEnviando(true);
    try {
      const actualizado = await authService.cambiarClave({
        claveActual: valores.actual,
        claveNueva: valores.nueva,
      });
      actualizarUsuario(actualizado);
      notificar({ tipo: "exito", titulo: "Contraseña actualizada", mensaje: "Ya puede usar su nueva contraseña." });
      navegar("/", { replace: true });
    } catch (fallo) {
      setErrorGeneral(fallo.message);
    } finally {
      setEnviando(false);
    }
  };

  const cerrarSesion = () => {
    logout();
    navegar("/login", { replace: true });
  };

  return (
    <div className="ingreso ingreso--clave">
      <section className="ingreso__marca ingreso__marca--compacta" aria-label="TechAsset">
        <div className="ingreso__logotipo">
          <span className="ingreso__icono" aria-hidden="true">
            <IconoLaptop />
          </span>
          <span>
            <strong>TechAsset</strong>
            <small>Seguridad de la cuenta</small>
          </span>
        </div>

        <div className="ingreso__mensaje">
          <h1>Proteja su cuenta corporativa.</h1>
          <p>
            {debeCambiarClave
              ? "Su cuenta fue creada con una contraseña temporal. Por seguridad, debe reemplazarla antes de continuar."
              : "Actualice su contraseña periódicamente para mantener segura su cuenta."}
          </p>
          <ul className="ingreso__beneficios">
            {REGLAS.map((regla) => (
              <li key={regla}>
                <span aria-hidden="true">
                  <IconoCheck tamano={18} />
                </span>
                {regla}
              </li>
            ))}
          </ul>
        </div>

        <p className="ingreso__pie">Innovatech Solutions S.A.C. · TechAsset · 2026</p>
      </section>

      <section className="ingreso__panel">
        <form className="ingreso__formulario" onSubmit={guardar} noValidate>
          <header className="ingreso__cabecera">
            <p className="ingreso__etiqueta">
              <IconoCandado tamano={16} /> Cuenta de {usuario?.nombreCompleto}
            </p>
            <h2>{debeCambiarClave ? "Cambio obligatorio de contraseña" : "Cambiar contraseña"}</h2>
            <p className="ingreso__ayuda">
              {debeCambiarClave
                ? "Defina una contraseña definitiva. La temporal dejará de funcionar."
                : "Ingrese su contraseña actual y defina una nueva."}
            </p>
          </header>

          {errorGeneral && (
            <div className="aviso aviso--error" role="alert">
              <IconoAlerta />
              <p>{errorGeneral}</p>
            </div>
          )}

          <CampoTexto id="actual" etiqueta="Contraseña actual" type="password" requerido autoComplete="current-password" value={valores.actual} onChange={actualizar("actual")} error={errores.actual} />
          <CampoTexto id="nueva" etiqueta="Nueva contraseña" type="password" requerido autoComplete="new-password" ayuda="Debe cumplir las cuatro reglas de seguridad." value={valores.nueva} onChange={actualizar("nueva")} error={errores.nueva} />
          <CampoTexto id="confirmar" etiqueta="Confirmar nueva contraseña" type="password" requerido autoComplete="new-password" value={valores.confirmar} onChange={actualizar("confirmar")} error={errores.confirmar} />

          <Boton type="submit" cargando={enviando} className="ingreso__enviar">
            {enviando ? "Guardando..." : "Actualizar contraseña"}
          </Boton>

          <div className="ingreso__acciones-secundarias">
            {debeCambiarClave ? (
              <button type="button" className="enlace-boton" onClick={cerrarSesion}>
                Cerrar sesión y volver al login
              </button>
            ) : (
              <Link to="/panel" className="enlace">
                Volver al panel
              </Link>
            )}
          </div>
        </form>

        <footer className="ingreso__panel-pie">© 2026 Innovatech Solutions S.A.C. · TechAsset</footer>
      </section>
    </div>
  );
}
