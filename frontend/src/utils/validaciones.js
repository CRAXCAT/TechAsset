import { AREAS, CATEGORIAS, ESTADOS_EQUIPO, ROLES } from "./constantes.js";
import { fechaDeHoyISO } from "./formato.js";

const CORREO = /^[a-zA-Z0-9._-]+@innovatech\.pe$/;

export function esClaveSegura(clave) {
  return (
    typeof clave === "string" &&
    clave.length >= 8 &&
    /[A-Z]/.test(clave) &&
    /[a-z]/.test(clave) &&
    /\d/.test(clave) &&
    /[^A-Za-z0-9]/.test(clave)
  );
}

export function validarUsuario(valores, esEdicion = false) {
  const errores = {};
  const nombres = valores.nombres.trim();
  const apellidos = valores.apellidos.trim();
  const correo = valores.correo.trim().toLowerCase();

  if (nombres.length < 3) errores.nombres = "Escriba los nombres (mínimo 3 caracteres).";
  if (apellidos.length < 3) errores.apellidos = "Escriba los apellidos (mínimo 3 caracteres).";

  if (!correo) {
    errores.correo = "El correo es obligatorio.";
  } else if (!CORREO.test(correo)) {
    errores.correo = "Use el formato nombre.apellido@innovatech.pe.";
  }

  if (!AREAS.includes(valores.area)) errores.area = "Seleccione un área.";
  if (!ROLES.some((r) => r.valor === valores.rol)) errores.rol = "Seleccione un rol.";

  if (!esEdicion && !esClaveSegura(valores.claveTemporal)) {
    errores.claveTemporal = "Mínimo 8 caracteres con mayúscula, minúscula, número y símbolo.";
  }

  return errores;
}

export function validarEquipo(valores) {
  const errores = {};
  const codigo = valores.codigoPatrimonial.trim();
  const nombre = valores.nombre.trim();
  const marca = valores.marca.trim();

  if (codigo.length < 3) errores.codigoPatrimonial = "El código patrimonial es obligatorio (mínimo 3 caracteres).";
  if (nombre.length < 3) errores.nombre = "El nombre del equipo es obligatorio (mínimo 3 caracteres).";
  if (!CATEGORIAS.includes(valores.categoria)) errores.categoria = "Seleccione una categoría.";
  if (marca.length < 2) errores.marca = "Indique la marca del equipo.";
  if (!ESTADOS_EQUIPO.some((e) => e.valor === valores.estado)) {
    errores.estado = "Seleccione el estado del equipo.";
  } else if (valores.estado === "Prestado") {
    errores.estado = "El estado Prestado se asigna automáticamente al registrar un préstamo.";
  }

  return errores;
}

export function validarPrestamo(valores) {
  const errores = {};

  if (!valores.usuarioId) errores.usuarioId = "Seleccione al colaborador.";
  if (!valores.equipoId) errores.equipoId = "Seleccione el equipo.";

  if (!valores.fechaPrestamo) {
    errores.fechaPrestamo = "Indique la fecha de préstamo.";
  }

  if (!valores.fechaDevolucion) {
    errores.fechaDevolucion = "Indique la fecha de devolución.";
  } else if (valores.fechaPrestamo && valores.fechaDevolucion <= valores.fechaPrestamo) {
    errores.fechaDevolucion = "La devolución debe ser posterior al préstamo (RN-04).";
  }

  const observacion = valores.observacion.trim();
  if (observacion.length < 5) {
    errores.observacion = "Registre el motivo del préstamo (mínimo 5 caracteres).";
  } else if (observacion.length > 300) {
    errores.observacion = "La observación no puede superar los 300 caracteres.";
  }

  return errores;
}

export function validarDevolucion(observacion) {
  const texto = observacion.trim();
  if (texto.length < 5) return "Toda devolución debe registrar observaciones (RN-10).";
  if (texto.length > 300) return "La observación no puede superar los 300 caracteres.";
  return "";
}

export function validarSolicitud(valores) {
  const errores = {};

  if (!valores.equipoId) errores.equipoId = "Seleccione el equipo.";

  if (!valores.fechaPrestamo) {
    errores.fechaPrestamo = "Indique la fecha de préstamo.";
  } else if (valores.fechaPrestamo < fechaDeHoyISO()) {
    errores.fechaPrestamo = "La fecha de préstamo no puede ser anterior a hoy.";
  }

  if (!valores.fechaDevolucion) {
    errores.fechaDevolucion = "Indique la fecha de devolución.";
  } else if (valores.fechaPrestamo && valores.fechaDevolucion <= valores.fechaPrestamo) {
    errores.fechaDevolucion = "La devolución debe ser posterior al préstamo (RN-04).";
  }

  const motivo = valores.motivo.trim();
  if (motivo.length < 5) {
    errores.motivo = "Registre el motivo de la solicitud (mínimo 5 caracteres).";
  } else if (motivo.length > 300) {
    errores.motivo = "El motivo no puede superar los 300 caracteres.";
  }

  return errores;
}

export { ESTADOS_EQUIPO };
