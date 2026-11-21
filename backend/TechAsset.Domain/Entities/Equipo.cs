namespace TechAsset.Domain.Entities;

public class Equipo
{
    public Guid Id { get; set; }
    public string CodigoPatrimonial { get; set; } = string.Empty;
    public string Nombre { get; set; } = string.Empty;
    public string Categoria { get; set; } = string.Empty;
    public string Marca { get; set; } = string.Empty;
    public string Estado { get; set; } = string.Empty;
    public DateTime FechaRegistro { get; set; }

    public ICollection<Prestamo> Prestamos { get; set; } = new List<Prestamo>();
    public ICollection<Solicitud> Solicitudes { get; set; } = new List<Solicitud>();
}
