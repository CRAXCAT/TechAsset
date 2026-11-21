namespace TechAsset.Domain.Entities;

public class Prestamo
{
    public Guid Id { get; set; }
    public DateOnly FechaPrestamo { get; set; }
    public DateOnly FechaDevolucion { get; set; }
    public DateOnly? FechaDevolucionReal { get; set; }
    public string Observacion { get; set; } = string.Empty;
    public string? ObservacionDevolucion { get; set; }
    public string Estado { get; set; } = string.Empty;

    public Guid UsuarioId { get; set; }
    public Usuario Usuario { get; set; } = null!;

    public Guid EquipoId { get; set; }
    public Equipo Equipo { get; set; } = null!;

    public Guid ResponsableId { get; set; }
    public Usuario Responsable { get; set; } = null!;

    public DateTime FechaRegistro { get; set; }

    public Solicitud? Solicitud { get; set; }
}
