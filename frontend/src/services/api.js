const URL_API = import.meta.env.VITE_API_URL ?? "http://localhost:5143/api";
const CLAVE_SESION = "techasset-sesion";

export class ErrorApi extends Error {
  constructor(mensaje, estado = 0, errores = null) {
    super(mensaje);
    this.name = "ErrorApi";
    this.estado = estado;
    this.errores = errores;
  }
}

function tokenActivo() {
  try {
    return JSON.parse(localStorage.getItem(CLAVE_SESION))?.token ?? null;
  } catch {
    return null;
  }
}

async function solicitar(ruta, { metodo = "GET", cuerpo } = {}) {
  let respuesta;
  const token = tokenActivo();

  try {
    respuesta = await fetch(`${URL_API}${ruta}`, {
      method: metodo,
      headers: {
        ...(cuerpo ? { "Content-Type": "application/json" } : {}),
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: cuerpo ? JSON.stringify(cuerpo) : undefined,
    });
  } catch {
    throw new ErrorApi(
      "No se pudo conectar con la API. Verifique que el servidor esté en ejecución en http://localhost:5143."
    );
  }

  const texto = await respuesta.text();
  let datos = null;

  if (texto) {
    try {
      datos = JSON.parse(texto);
    } catch {
      datos = null;
    }
  }

  if (!respuesta.ok) {
    if (respuesta.status === 401 && !ruta.startsWith("/auth/login")) {
      window.dispatchEvent(new Event("sesion-expirada"));
    }

    throw new ErrorApi(
      datos?.mensaje ?? "La operación no se pudo completar. Intente nuevamente.",
      respuesta.status,
      datos?.errores ?? null
    );
  }

  return datos;
}

export const api = {
  obtener: (ruta) => solicitar(ruta),
  crear: (ruta, cuerpo) => solicitar(ruta, { metodo: "POST", cuerpo }),
  actualizar: (ruta, cuerpo) => solicitar(ruta, { metodo: "PATCH", cuerpo }),
  reemplazar: (ruta, cuerpo) => solicitar(ruta, { metodo: "PUT", cuerpo }),
  eliminar: (ruta) => solicitar(ruta, { metodo: "DELETE" }),
  descargar: async (ruta) => {
    const token = tokenActivo();
    const respuesta = await fetch(`${URL_API}${ruta}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : undefined,
    });

    if (!respuesta.ok) {
      throw new ErrorApi("No se pudo generar el reporte.", respuesta.status);
    }

    return respuesta.blob();
  },
};
