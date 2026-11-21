namespace TechAsset.Domain.Entities;

/// <summary>
/// Petición de un colaborador para recibir un equipo. El Responsable de
/// Tecnología la aprueba o rechaza; la aprobación genera un préstamo.
/// </summary>
public class Solicitud
{
    public Guid Id { get; set; }
    public DateOnly FechaPrestamo { get; set; }
    public DateOnly FechaDevolucion { get; set; }
    public string Motivo { get; set; } = string.Empty;
    public string Estado { get; set; } = string.Empty;
    public string? ObservacionRevision { get; set; }

    public Guid UsuarioId { get; set; }
    public Usuario Usuario { get; set; } = null!;

    public Guid EquipoId { get; set; }
    public Equipo Equipo { get; set; } = null!;

    public Guid? PrestamoId { get; set; }
    public Prestamo? Prestamo { get; set; }

    public Guid? RevisadoPorId { get; set; }
    public Usuario? RevisadoPor { get; set; }

    public DateTime FechaRegistro { get; set; }
    public DateTime? FechaRevision { get; set; }
}
