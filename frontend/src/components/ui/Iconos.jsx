/**
 * Iconos SVG propios: sin dependencias externas, heredan el color del texto
 * y se ocultan a los lectores de pantalla porque siempre acompañan una etiqueta.
 */
function Svg({ children, tamano = 20, ...props }) {
  return (
    <svg
      width={tamano}
      height={tamano}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      focusable="false"
      {...props}
    >
      {children}
    </svg>
  );
}

export const IconoInicio = (props) => (
  <Svg {...props}>
    <path d="M3 10.5 12 3l9 7.5" />
    <path d="M5.5 9.5V21h13V9.5" />
    <path d="M9.5 21v-6h5v6" />
  </Svg>
);

export const IconoNuevo = (props) => (
  <Svg {...props}>
    <rect x="3" y="3" width="18" height="18" rx="3" />
    <path d="M12 8v8M8 12h8" />
  </Svg>
);

export const IconoLista = (props) => (
  <Svg {...props}>
    <path d="M8 6h13M8 12h13M8 18h13" />
    <circle cx="3.5" cy="6" r="1" />
    <circle cx="3.5" cy="12" r="1" />
    <circle cx="3.5" cy="18" r="1" />
  </Svg>
);

export const IconoRayo = (props) => (
  <Svg {...props}>
    <path d="M13 2 4.5 13.5H11l-1 8.5L19.5 10H13z" />
  </Svg>
);

export const IconoSol = (props) => (
  <Svg {...props}>
    <circle cx="12" cy="12" r="4" />
    <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
  </Svg>
);

export const IconoLuna = (props) => (
  <Svg {...props}>
    <path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5Z" />
  </Svg>
);

export const IconoMenu = (props) => (
  <Svg {...props}>
    <path d="M4 6h16M4 12h16M4 18h16" />
  </Svg>
);

export const IconoCerrar = (props) => (
  <Svg {...props}>
    <path d="M6 6l12 12M18 6 6 18" />
  </Svg>
);

export const IconoBuscar = (props) => (
  <Svg {...props}>
    <circle cx="11" cy="11" r="7" />
    <path d="m16.5 16.5 4 4" />
  </Svg>
);

export const IconoOjo = (props) => (
  <Svg {...props}>
    <path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12Z" />
    <circle cx="12" cy="12" r="2.8" />
  </Svg>
);

export const IconoBaseDatos = (props) => (
  <Svg {...props}>
    <ellipse cx="12" cy="5.5" rx="8" ry="3" />
    <path d="M4 5.5v13c0 1.7 3.6 3 8 3s8-1.3 8-3v-13" />
    <path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3" />
  </Svg>
);

export const IconoServidor = (props) => (
  <Svg {...props}>
    <rect x="3" y="4" width="18" height="6.5" rx="2" />
    <rect x="3" y="13.5" width="18" height="6.5" rx="2" />
    <path d="M7 7.2h.01M7 16.7h.01" />
  </Svg>
);

export const IconoCheck = (props) => (
  <Svg {...props}>
    <path d="m4.5 12.5 5 5 10-11" />
  </Svg>
);

export const IconoAlerta = (props) => (
  <Svg {...props}>
    <path d="M12 3.5 22 20H2z" />
    <path d="M12 9.5v5M12 17.5h.01" />
  </Svg>
);

export const IconoInfo = (props) => (
  <Svg {...props}>
    <circle cx="12" cy="12" r="9" />
    <path d="M12 11v5M12 8h.01" />
  </Svg>
);

export const IconoReloj = (props) => (
  <Svg {...props}>
    <circle cx="12" cy="12" r="9" />
    <path d="M12 7v5.3l3.2 1.9" />
  </Svg>
);

export const IconoTicket = (props) => (
  <Svg {...props}>
    <path d="M3 8.5V7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v1.5a3.5 3.5 0 0 0 0 7V17a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1.5a3.5 3.5 0 0 0 0-7Z" />
    <path d="M14 5v14" strokeDasharray="2 3" />
  </Svg>
);

export const IconoUsuario = (props) => (
  <Svg {...props}>
    <circle cx="12" cy="8" r="4" />
    <path d="M4.5 21a7.5 7.5 0 0 1 15 0" />
  </Svg>
);

export const IconoFiltro = (props) => (
  <Svg {...props}>
    <path d="M3 5h18l-7 8v6l-4 2v-8z" />
  </Svg>
);

export const IconoRefrescar = (props) => (
  <Svg {...props}>
    <path d="M20 11a8 8 0 1 0-2.5 6.4" />
    <path d="M20 4v7h-7" />
  </Svg>
);

export const IconoFlechaIzquierda = (props) => (
  <Svg {...props}>
    <path d="M15 5 8 12l7 7" />
  </Svg>
);

export const IconoFlechaDerecha = (props) => (
  <Svg {...props}>
    <path d="m9 5 7 7-7 7" />
  </Svg>
);

export const IconoFlechaAbajo = (props) => (
  <Svg {...props}>
    <path d="m5 9 7 7 7-7" />
  </Svg>
);

export const IconoDescargar = (props) => (
  <Svg {...props}>
    <path d="M12 3v12M7 10l5 5 5-5" />
    <path d="M4 19h16" />
  </Svg>
);

export const IconoEdificio = (props) => (
  <Svg {...props}>
    <path d="M4 21V6l8-3 8 3v15" />
    <path d="M4 21h16" />
    <path d="M9 9h1M14 9h1M9 13h1M14 13h1M9 17h1M14 17h1" />
  </Svg>
);

export const IconoUsuarios = (props) => (
  <Svg {...props}>
    <circle cx="9" cy="8" r="3.5" />
    <path d="M2.5 20a6.5 6.5 0 0 1 13 0" />
    <path d="M16 5.5a3.5 3.5 0 0 1 0 6.6" />
    <path d="M17.5 14.2A5.5 5.5 0 0 1 21.5 20" />
  </Svg>
);

export const IconoCalendario = (props) => (
  <Svg {...props}>
    <rect x="3" y="5" width="18" height="16" rx="3" />
    <path d="M8 3v4M16 3v4M3 10h18" />
    <path d="M8 14h2M14 14h2M8 17h2M14 17h2" />
  </Svg>
);

export const IconoAyuda = (props) => (
  <Svg {...props}>
    <circle cx="12" cy="12" r="9" />
    <path d="M9.5 9.2a2.6 2.6 0 0 1 5.1.6c0 1.8-2.6 2.2-2.6 4" />
    <path d="M12 17.4h.01" />
  </Svg>
);

export const IconoTeclado = (props) => (
  <Svg {...props}>
    <rect x="2.5" y="6" width="19" height="12" rx="3" />
    <path d="M6 10h.01M9.5 10h.01M13 10h.01M16.5 10h.01M6 13.5h.01M18 13.5h.01M9.5 14h5" />
  </Svg>
);

export const IconoCandado = (props) => (
  <Svg {...props}>
    <rect x="4" y="10" width="16" height="11" rx="2" />
    <path d="M8 10V7a4 4 0 0 1 8 0v3" />
    <path d="M12 14v3" />
  </Svg>
);

export const IconoSalir = (props) => (
  <Svg {...props}>
    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
    <path d="m16 17 5-5-5-5M21 12H9" />
  </Svg>
);

export const IconoEscudo = (props) => (
  <Svg {...props}>
    <path d="M12 3 5 6v5.5c0 4.6 3 8.2 7 9.5 4-1.3 7-4.9 7-9.5V6l-7-3Z" />
    <path d="m9 12 2 2 4-4" />
  </Svg>
);

export const IconoLaptop = (props) => (
  <Svg {...props}>
    <rect x="4" y="5" width="16" height="11" rx="2" />
    <path d="M2.5 19h19M9 16h6" />
  </Svg>
);

export const IconoGrafico = (props) => (
  <Svg {...props}>
    <path d="M4 20V10M10 20V4M16 20v-7M22 20H2" />
  </Svg>
);

export const IconoDevolver = (props) => (
  <Svg {...props}>
    <path d="M9 14 4 9l5-5" />
    <path d="M4 9h10a6 6 0 0 1 0 12h-3" />
  </Svg>
);
