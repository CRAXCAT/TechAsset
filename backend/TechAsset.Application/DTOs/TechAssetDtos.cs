using System.ComponentModel.DataAnnotations;

namespace TechAsset.Application.DTOs;

// --------------------------------------------------------------------------
// Usuarios
// --------------------------------------------------------------------------
public class CrearUsuarioDto
{
    [Required(ErrorMessage = "Los nombres son obligatorios.")]
    [StringLength(100, MinimumLength = 3, ErrorMessage = "Los nombres deben tener entre 3 y 100 caracteres.")]
    public string Nombres { get; set; } = string.Empty;

    [Required(ErrorMessage = "Los apellidos son obligatorios.")]
    [StringLength(100, MinimumLength = 3, ErrorMessage = "Los apellidos deben tener entre 3 y 100 caracteres.")]
    public string Apellidos { get; set; } = string.Empty;

    [Required(ErrorMessage = "El correo es obligatorio.")]
    [EmailAddress(ErrorMessage = "El correo no tiene un formato válido.")]
    [RegularExpression(@"^[a-zA-Z0-9._-]+@innovatech\.pe$", ErrorMessage = "El correo debe pertenecer al dominio @innovatech.pe.")]
    public string Correo { get; set; } = string.Empty;

    [Required(ErrorMessage = "Seleccione un área.")]
    public string Area { get; set; } = string.Empty;

    [Required(ErrorMessage = "Seleccione un rol.")]
    public string Rol { get; set; } = string.Empty;

    [Required(ErrorMessage = "Defina una contraseña temporal.")]
    [RegularExpression(@"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$", ErrorMessage = "La contraseña temporal debe tener al menos 8 caracteres, con mayúscula, minúscula, número y símbolo.")]
    public string ClaveTemporal { get; set; } = string.Empty;
}

public class ActualizarUsuarioDto
{
    [Required(ErrorMessage = "Los nombres son obligatorios.")]
    [StringLength(100, MinimumLength = 3, ErrorMessage = "Los nombres deben tener entre 3 y 100 caracteres.")]
    public string Nombres { get; set; } = string.Empty;

    [Required(ErrorMessage = "Los apellidos son obligatorios.")]
    [StringLength(100, MinimumLength = 3, ErrorMessage = "Los apellidos deben tener entre 3 y 100 caracteres.")]
    public string Apellidos { get; set; } = string.Empty;

    [Required(ErrorMessage = "El correo es obligatorio.")]
    [EmailAddress(ErrorMessage = "El correo no tiene un formato válido.")]
    [RegularExpression(@"^[a-zA-Z0-9._-]+@innovatech\.pe$", ErrorMessage = "El correo debe pertenecer al dominio @innovatech.pe.")]
    public string Correo { get; set; } = string.Empty;

    [Required(ErrorMessage = "Seleccione un área.")]
    public string Area { get; set; } = string.Empty;

    [Required(ErrorMessage = "Seleccione un rol.")]
    public string Rol { get; set; } = string.Empty;
}

public class UsuarioDto
{
    public Guid Id { get; set; }
    public string Nombres { get; set; } = string.Empty;
    public string Apellidos { get; set; } = string.Empty;
    public string NombreCompleto { get; set; } = string.Empty;
    public string Correo { get; set; } = string.Empty;
    public string Area { get; set; } = string.Empty;
    public string Rol { get; set; } = string.Empty;
    public bool Activo { get; set; }
    public bool DebeCambiarPassword { get; set; }
    public DateTime FechaRegistro { get; set; }
}

// --------------------------------------------------------------------------
// Equipos
// --------------------------------------------------------------------------
public class CrearEquipoDto
{
    [Required(ErrorMessage = "El código patrimonial es obligatorio.")]
    [StringLength(50, MinimumLength = 3, ErrorMessage = "El código debe tener entre 3 y 50 caracteres.")]
    public string CodigoPatrimonial { get; set; } = string.Empty;

    [Required(ErrorMessage = "El nombre del equipo es obligatorio.")]
    [StringLength(100, MinimumLength = 3, ErrorMessage = "El nombre debe tener entre 3 y 100 caracteres.")]
    public string Nombre { get; set; } = string.Empty;

    [Required(ErrorMessage = "Seleccione una categoría.")]
    public string Categoria { get; set; } = string.Empty;

    [Required(ErrorMessage = "La marca es obligatoria.")]
    [StringLength(50, MinimumLength = 2, ErrorMessage = "La marca debe tener entre 2 y 50 caracteres.")]
    public string Marca { get; set; } = string.Empty;

    [Required(ErrorMessage = "Seleccione el estado del equipo.")]
    public string Estado { get; set; } = string.Empty;
}

public class CambiarEstadoEquipoDto
{
    [Required(ErrorMessage = "Indique el nuevo estado.")]
    public string Estado { get; set; } = string.Empty;
}

public class EquipoDto
{
    public Guid Id { get; set; }
    public string CodigoPatrimonial { get; set; } = string.Empty;
    public string Nombre { get; set; } = string.Empty;
    public string Categoria { get; set; } = string.Empty;
    public string Marca { get; set; } = string.Empty;
    public string Estado { get; set; } = string.Empty;
    public bool PrestamoActivo { get; set; }
    public int TotalPrestamos { get; set; }
    public DateTime FechaRegistro { get; set; }
}

// --------------------------------------------------------------------------
// Préstamos
// --------------------------------------------------------------------------
public class CrearPrestamoDto
{
    [Required(ErrorMessage = "Seleccione al colaborador.")]
    public Guid UsuarioId { get; set; }

    [Required(ErrorMessage = "Seleccione el equipo.")]
    public Guid EquipoId { get; set; }

    [Required(ErrorMessage = "Indique la fecha de préstamo.")]
    public DateOnly FechaPrestamo { get; set; }

    [Required(ErrorMessage = "Indique la fecha de devolución.")]
    public DateOnly FechaDevolucion { get; set; }

    [Required(ErrorMessage = "La observación es obligatoria.")]
    [StringLength(300, MinimumLength = 5, ErrorMessage = "La observación debe tener entre 5 y 300 caracteres.")]
    public string Observacion { get; set; } = string.Empty;
}

public class DevolverPrestamoDto
{
    [Required(ErrorMessage = "Registre la observación de la devolución.")]
    [StringLength(300, MinimumLength = 5, ErrorMessage = "La observación de devolución debe tener entre 5 y 300 caracteres.")]
    public string ObservacionDevolucion { get; set; } = string.Empty;
}

public class PrestamoDto
{
    public Guid Id { get; set; }
    public string Codigo { get; set; } = string.Empty;
    public DateOnly FechaPrestamo { get; set; }
    public DateOnly FechaDevolucion { get; set; }
    public DateOnly? FechaDevolucionReal { get; set; }
    public string Observacion { get; set; } = string.Empty;
    public string? ObservacionDevolucion { get; set; }
    public string Estado { get; set; } = string.Empty;
    public Guid UsuarioId { get; set; }
    public string Solicitante { get; set; } = string.Empty;
    public string Area { get; set; } = string.Empty;
    public Guid EquipoId { get; set; }
    public string Equipo { get; set; } = string.Empty;
    public string CodigoPatrimonial { get; set; } = string.Empty;
    public string Categoria { get; set; } = string.Empty;
    public Guid ResponsableId { get; set; }
    public string Responsable { get; set; } = string.Empty;
    public DateTime FechaRegistro { get; set; }
}

// --------------------------------------------------------------------------
// Solicitudes
// --------------------------------------------------------------------------
public class CrearSolicitudDto
{
    [Required(ErrorMessage = "Seleccione el equipo.")]
    public Guid EquipoId { get; set; }

    [Required(ErrorMessage = "Indique la fecha de préstamo.")]
    public DateOnly FechaPrestamo { get; set; }

    [Required(ErrorMessage = "Indique la fecha de devolución.")]
    public DateOnly FechaDevolucion { get; set; }

    [Required(ErrorMessage = "Registre el motivo de la solicitud.")]
    [StringLength(300, MinimumLength = 5, ErrorMessage = "El motivo debe tener entre 5 y 300 caracteres.")]
    public string Motivo { get; set; } = string.Empty;
}

public class RevisarSolicitudDto
{
    [StringLength(300, ErrorMessage = "La observación no puede superar los 300 caracteres.")]
    public string? ObservacionRevision { get; set; }
}

public class SolicitudDto
{
    public Guid Id { get; set; }
    public string Codigo { get; set; } = string.Empty;
    public DateOnly FechaPrestamo { get; set; }
    public DateOnly FechaDevolucion { get; set; }
    public string Motivo { get; set; } = string.Empty;
    public string Estado { get; set; } = string.Empty;
    public string? ObservacionRevision { get; set; }
    public Guid UsuarioId { get; set; }
    public string Solicitante { get; set; } = string.Empty;
    public string Area { get; set; } = string.Empty;
    public Guid EquipoId { get; set; }
    public string Equipo { get; set; } = string.Empty;
    public string CodigoPatrimonial { get; set; } = string.Empty;
    public string Categoria { get; set; } = string.Empty;
    public Guid? PrestamoId { get; set; }
    public string? CodigoPrestamo { get; set; }
    public Guid? RevisadoPorId { get; set; }
    public string? Revisor { get; set; }
    public DateTime FechaRegistro { get; set; }
    public DateTime? FechaRevision { get; set; }
}

// --------------------------------------------------------------------------
// Movimientos
// --------------------------------------------------------------------------
public class MovimientoDto
{
    public Guid Id { get; set; }
    public DateTime Fecha { get; set; }
    public string Entidad { get; set; } = string.Empty;
    public Guid EntidadId { get; set; }
    public string Accion { get; set; } = string.Empty;
    public string Detalle { get; set; } = string.Empty;
    public Guid? UsuarioId { get; set; }
    public string UsuarioNombre { get; set; } = string.Empty;
}

// --------------------------------------------------------------------------
// Reportes
// --------------------------------------------------------------------------
public class UsoDto
{
    public string Etiqueta { get; set; } = string.Empty;
    public int Total { get; set; }
}

public class ResumenTechAssetDto
{
    public int TotalEquipos { get; set; }
    public int Disponibles { get; set; }
    public int Prestados { get; set; }
    public int Mantenimiento { get; set; }
    public int Bajas { get; set; }
    public int TotalPrestamos { get; set; }
    public int PrestamosActivos { get; set; }
    public int PrestamosDevueltos { get; set; }
    public int TotalSolicitudes { get; set; }
    public int SolicitudesPendientes { get; set; }
    public int SolicitudesAprobadas { get; set; }
    public int SolicitudesRechazadas { get; set; }
    public string AreaMayorUso { get; set; } = "Sin datos";
    public int PrestamosAreaMayor { get; set; }
    public IReadOnlyList<UsoDto> PrestamosPorArea { get; set; } = Array.Empty<UsoDto>();
    public IReadOnlyList<UsoDto> EquiposPorEstado { get; set; } = Array.Empty<UsoDto>();
    public IReadOnlyList<UsoDto> EquiposMasUtilizados { get; set; } = Array.Empty<UsoDto>();
}
