namespace TechAsset.Domain.Entities;

/// <summary>
/// Registro de auditoría de las operaciones relevantes. Guarda una instantánea
/// del nombre del actor para conservar el contexto aunque la cuenta cambie.
/// </summary>
public class Movimiento
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
