namespace TechAsset.Domain.Constantes;

/// <summary>
/// Catálogo único de roles, áreas, categorías y estados. Centralizar los valores
/// evita cadenas duplicadas entre capas y mantiene la consistencia del sistema.
/// </summary>
public static class CatalogoTechAsset
{
    public const string RolAdministrador = "Administrador";
    public const string RolResponsable = "Responsable";
    public const string RolColaborador = "Colaborador";

    public static readonly IReadOnlyList<string> Roles = new[]
    {
        RolAdministrador,
        RolResponsable,
        RolColaborador
    };

    public static readonly IReadOnlyList<string> Areas = new[]
    {
        "Desarrollo",
        "Sistemas",
        "Soporte",
        "Recursos Humanos",
        "Contabilidad",
        "Marketing",
        "Gerencia"
    };

    public static readonly IReadOnlyList<string> Categorias = new[]
    {
        "Laptop",
        "Computadora de escritorio",
        "Monitor",
        "Impresora",
        "Tablet",
        "Proyector",
        "Equipo de red"
    };

    public const string EquipoDisponible = "Disponible";
    public const string EquipoPrestado = "Prestado";
    public const string EquipoMantenimiento = "Mantenimiento";
    public const string EquipoBaja = "Baja";

    public static readonly IReadOnlyList<string> EstadosEquipo = new[]
    {
        EquipoDisponible,
        EquipoPrestado,
        EquipoMantenimiento,
        EquipoBaja
    };

    public const string PrestamoActivo = "Activo";
    public const string PrestamoDevuelto = "Devuelto";

    public static readonly IReadOnlyList<string> EstadosPrestamo = new[]
    {
        PrestamoActivo,
        PrestamoDevuelto
    };

    public const string SolicitudPendiente = "Pendiente";
    public const string SolicitudAprobada = "Aprobada";
    public const string SolicitudRechazada = "Rechazada";

    public static readonly IReadOnlyList<string> EstadosSolicitud = new[]
    {
        SolicitudPendiente,
        SolicitudAprobada,
        SolicitudRechazada
    };

    public static bool EsRolValido(string rol) => Roles.Contains(rol);
    public static bool EsAreaValida(string area) => Areas.Contains(area);
    public static bool EsCategoriaValida(string categoria) => Categorias.Contains(categoria);
    public static bool EsEstadoEquipoValido(string estado) => EstadosEquipo.Contains(estado);
    public static bool EsEstadoPrestamoValido(string estado) => EstadosPrestamo.Contains(estado);
    public static bool EsEstadoSolicitudValido(string estado) => EstadosSolicitud.Contains(estado);


    /// <summary>Estados que impiden registrar un préstamo (RN-02 y RN-03).</summary>
    public static bool BloqueaPrestamo(string estado) => estado is EquipoMantenimiento or EquipoBaja;
}
