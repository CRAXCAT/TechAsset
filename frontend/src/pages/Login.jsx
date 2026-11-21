import { useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import Boton from "../components/ui/Boton.jsx";
import CampoTexto from "../components/ui/CampoTexto.jsx";
import {
  IconoAlerta,
  IconoCheck,
  IconoDevolver,
  IconoLaptop,
  IconoInfo,
  IconoOjo,
  IconoEscudo,
  IconoFlechaIzquierda,
} from "../components/ui/Iconos.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { ErrorApi } from "../services/api.js";

const BENEFICIOS = [
  { Icono: IconoLaptop, texto: "Consulte la disponibilidad real de laptops, monitores e impresoras." },
  { Icono: IconoDevolver, texto: "Registre préstamos y devoluciones con trazabilidad completa." },
  { Icono: IconoEscudo, texto: "Cada rol accede solo a las acciones que le corresponden." },
];

export default function Login() {
  const { sesion, login } = useAuth();
  const navegar = useNavigate();
  const ubicacion = useLocation();
  const destino = ubicacion.state?.desde ?? "/panel";

  const [correo, setCorreo] = useState("");
  const [clave, setClave] = useState("");
  const [verClave, setVerClave] = useState(false);
  const [bloqMayus, setBloqMayus] = useState(false);
  const [errores, setErrores] = useState({});
  const [errorGeneral, setErrorGeneral] = useState("");
  const [enviando, setEnviando] = useState(false);

  if (sesion) {
    return <Navigate to={sesion.usuario?.debeCambiarPassword ? "/cambiar-clave" : destino} replace />;
  }

  const validar = () => {
    const encontrados = {};
    if (!correo.trim()) {
      encontrados.correo = "Ingrese su correo corporativo.";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo.trim())) {
      encontrados.correo = "El correo debe tener el formato nombre.apellido@innovatech.pe.";
    }
    if (!clave) encontrados.clave = "Ingrese su contraseña.";
    return encontrados;
  };

  const ingresar = async (evento) => {
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
      const datos = await login(correo.trim().toLowerCase(), clave);
      navegar(datos.usuario.debeCambiarPassword ? "/cambiar-clave" : destino, { replace: true });
    } catch (fallo) {
      setErrorGeneral(
        fallo instanceof ErrorApi && fallo.estado === 401
          ? "Correo o contraseña incorrectos. Verifique sus datos e intente nuevamente."
          : fallo.message
      );
    } finally {
      setEnviando(false);
    }
  };

  const limpiar = () => {
    setCorreo("");
    setClave("");
    setErrores({});
    setErrorGeneral("");
    setBloqMayus(false);
    document.getElementById("correo")?.focus();
  };

  const detectarBloqMayus = (evento) => {
    if (typeof evento.getModifierState === "function") {
      setBloqMayus(evento.getModifierState("CapsLock"));
    }
  };

  return (
    <div className="ingreso">
      <section className="ingreso__marca" aria-label="TechAsset">
        <div className="ingreso__logotipo">
          <span className="ingreso__icono" aria-hidden="true">
            <IconoLaptop />
          </span>
          <span>
            <strong>TechAsset</strong>
            <small>Inventario y préstamo de equipos</small>
          </span>
        </div>

        <div className="ingreso__mensaje">
          <h1>Controle el inventario y los préstamos de equipos.</h1>
          <p>
            Sistema corporativo de Innovatech Solutions para administrar activos tecnológicos, asignar equipos y registrar
            devoluciones con trazabilidad.
          </p>

          <ul className="ingreso__beneficios">
            {BENEFICIOS.map(({ Icono, texto }) => (
              <li key={texto}>
                <span aria-hidden="true">
                  <Icono tamano={18} />
                </span>
                {texto}
              </li>
            ))}
          </ul>
        </div>

        <p className="ingreso__pie">Innovatech Solutions S.A.C. · TechAsset · 2026</p>
      </section>

      <section className="ingreso__panel">
        <header className="ingreso__panel-cabecera">
          <Link to="/" className="ingreso__volver">
            <IconoFlechaIzquierda tamano={16} />
            Volver al portal
          </Link>
          <a className="ingreso__soporte" href="mailto:soporte@innovatech.pe">
            soporte@innovatech.pe
          </a>
        </header>

        <form className="ingreso__formulario" onSubmit={ingresar} noValidate>
          <header className="ingreso__cabecera">
            <p className="ingreso__etiqueta">Cuenta corporativa</p>
            <h2>Iniciar sesión</h2>
            <p className="ingreso__ayuda">
              Ingrese con su correo <strong>@innovatech.pe</strong> y la contraseña asignada por el administrador.
            </p>
          </header>

          {errorGeneral && (
            <div className="aviso aviso--error" role="alert">
              <IconoAlerta />
              <p>{errorGeneral}</p>
            </div>
          )}

          <CampoTexto
            id="correo"
            etiqueta="Correo corporativo"
            type="email"
            requerido
            autoFocus
            autoComplete="username"
            inputMode="email"
            placeholder="nombre.apellido@innovatech.pe"
            ayuda="Ejemplo: ana.torres@innovatech.pe"
            value={correo}
            onChange={(evento) => {
              setCorreo(evento.target.value);
              setErrores((actuales) => ({ ...actuales, correo: undefined }));
            }}
            error={errores.correo}
          />

          <div>
            <CampoTexto
              id="clave"
              etiqueta="Contraseña"
              type={verClave ? "text" : "password"}
              requerido
              autoComplete="current-password"
              placeholder="Ingrese su contraseña"
              value={clave}
              onChange={(evento) => {
                setClave(evento.target.value);
                setErrores((actuales) => ({ ...actuales, clave: undefined }));
              }}
              onKeyUp={detectarBloqMayus}
              onKeyDown={detectarBloqMayus}
              error={errores.clave}
              sufijo={
                <button
                  type="button"
                  className="campo__boton-sufijo"
                  onClick={() => setVerClave((actual) => !actual)}
                  aria-pressed={verClave}
                  aria-label={verClave ? "Ocultar la contraseña" : "Mostrar la contraseña"}
                  title={verClave ? "Ocultar la contraseña" : "Mostrar la contraseña"}
                >
                  <IconoOjo tamano={20} />
                </button>
              }
            />

            {bloqMayus && (
              <p className="ingreso__aviso-mayus" role="status">
                <IconoAlerta tamano={16} />
                Bloq Mayús está activado. La contraseña distingue mayúsculas de minúsculas.
              </p>
            )}
          </div>

          <Boton type="submit" cargando={enviando} className="ingreso__enviar">
            {enviando ? "Verificando credenciales..." : "Ingresar"}
          </Boton>

          <div className="ingreso__enlaces">
            <button type="button" className="enlace-boton" onClick={limpiar}>
              Limpiar campos
            </button>
            <a className="enlace-boton" href="mailto:soporte@innovatech.pe?subject=Recuperaci%C3%B3n%20de%20acceso">
              ¿Olvidó su contraseña?
            </a>
          </div>

          <p className="ingreso__nota">
            <IconoInfo tamano={14} />
            Acceso exclusivo para cuentas corporativas. Si no puede ingresar, escriba a soporte@innovatech.pe.
          </p>
        </form>

        <footer className="ingreso__panel-pie">© 2026 Innovatech Solutions S.A.C. · TechAsset</footer>
      </section>
    </div>
  );
}
