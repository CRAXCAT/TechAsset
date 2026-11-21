export const ROLES = [
  { valor: "Administrador", descripcion: "Gestiona usuarios, equipos, préstamos y reportes" },
  { valor: "Responsable", descripcion: "Registra equipos, préstamos y devoluciones" },
  { valor: "Colaborador", descripcion: "Consulta disponibilidad y su historial" },
];

export const AREAS = [
  "Desarrollo",
  "Sistemas",
  "Soporte",
  "Recursos Humanos",
  "Contabilidad",
  "Marketing",
  "Gerencia",
];

export const CATEGORIAS = [
  "Laptop",
  "Computadora de escritorio",
  "Monitor",
  "Impresora",
  "Tablet",
  "Proyector",
  "Equipo de red",
];

export const ESTADOS_EQUIPO = [
  { valor: "Disponible", tono: "verde", descripcion: "Listo para préstamo" },
  { valor: "Prestado", tono: "azul", descripcion: "Asignado a un colaborador" },
  { valor: "Mantenimiento", tono: "ambar", descripcion: "Fuera de servicio temporalmente" },
  { valor: "Baja", tono: "rojo", descripcion: "Retirado del inventario" },
];

export const ESTADOS_PRESTAMO = [
  { valor: "Activo", tono: "ambar", descripcion: "Equipo entregado, pendiente de devolución" },
  { valor: "Devuelto", tono: "verde", descripcion: "Equipo devuelto y disponible" },
];

export const ESTADOS_SOLICITUD = [
  { valor: "Pendiente", tono: "ambar", descripcion: "Esperando revisión del Responsable" },
  { valor: "Aprobada", tono: "verde", descripcion: "Aprobada y convertida en préstamo" },
  { valor: "Rechazada", tono: "rojo", descripcion: "Rechazada con observación" },
];

export const TONO_EQUIPO = Object.fromEntries(ESTADOS_EQUIPO.map((e) => [e.valor, e.tono]));
export const TONO_PRESTAMO = Object.fromEntries(ESTADOS_PRESTAMO.map((e) => [e.valor, e.tono]));
export const TONO_SOLICITUD = Object.fromEntries(ESTADOS_SOLICITUD.map((e) => [e.valor, e.tono]));

export const HORIZONTE_DIAS = 30;
export const TAMANO_PAGINA = 8;
