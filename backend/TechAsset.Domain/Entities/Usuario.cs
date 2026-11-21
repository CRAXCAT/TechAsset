namespace TechAsset.Domain.Entities;

public class Usuario
{
    public Guid Id { get; set; }
    public string Nombres { get; set; } = string.Empty;
    public string Apellidos { get; set; } = string.Empty;
    public string Correo { get; set; } = string.Empty;
    public string Area { get; set; } = string.Empty;
    public string Rol { get; set; } = string.Empty;
    public bool Activo { get; set; } = true;
    public string PasswordHash { get; set; } = string.Empty;
    public bool DebeCambiarPassword { get; set; }
    public DateTime FechaRegistro { get; set; }

    public ICollection<Prestamo> Prestamos { get; set; } = new List<Prestamo>();
    public ICollection<Prestamo> PrestamosResponsable { get; set; } = new List<Prestamo>();
    public ICollection<Solicitud> Solicitudes { get; set; } = new List<Solicitud>();
    public ICollection<Solicitud> SolicitudesRevisadas { get; set; } = new List<Solicitud>();
}
