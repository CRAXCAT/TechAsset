namespace TechAsset.Application.Models;

public class FiltroUsuarios
{
    public string? Texto { get; set; }
    public string? Area { get; set; }
    public string? Rol { get; set; }
    public bool? Activo { get; set; }

    public void Normalizar()
    {
        Texto = string.IsNullOrWhiteSpace(Texto) ? null : Texto.Trim();
        Area = string.IsNullOrWhiteSpace(Area) ? null : Area.Trim();
        Rol = string.IsNullOrWhiteSpace(Rol) ? null : Rol.Trim();
    }
}

public class FiltroEquipos
{
    public string? Texto { get; set; }
    public string? Categoria { get; set; }
    public string? Estado { get; set; }

    public void Normalizar()
    {
        Texto = string.IsNullOrWhiteSpace(Texto) ? null : Texto.Trim();
        Categoria = string.IsNullOrWhiteSpace(Categoria) ? null : Categoria.Trim();
        Estado = string.IsNullOrWhiteSpace(Estado) ? null : Estado.Trim();
    }
}

public class FiltroPrestamos
{
    public string? Texto { get; set; }
    public string? Estado { get; set; }
    public string? Area { get; set; }
    public Guid? EquipoId { get; set; }
    public DateOnly? Desde { get; set; }
    public DateOnly? Hasta { get; set; }
    public int Pagina { get; set; } = 1;
    public int TamanoPagina { get; set; } = 8;

    public void Normalizar()
    {
        Texto = string.IsNullOrWhiteSpace(Texto) ? null : Texto.Trim();
        Estado = string.IsNullOrWhiteSpace(Estado) ? null : Estado.Trim();
        Area = string.IsNullOrWhiteSpace(Area) ? null : Area.Trim();
        Pagina = Pagina < 1 ? 1 : Pagina;
        TamanoPagina = TamanoPagina is < 1 or > 100 ? 8 : TamanoPagina;
    }
}

public class FiltroSolicitudes
{
    public string? Texto { get; set; }
    public string? Estado { get; set; }
    public string? Area { get; set; }
    public Guid? EquipoId { get; set; }
    public int Pagina { get; set; } = 1;
    public int TamanoPagina { get; set; } = 8;

    public void Normalizar()
    {
        Texto = string.IsNullOrWhiteSpace(Texto) ? null : Texto.Trim();
        Estado = string.IsNullOrWhiteSpace(Estado) ? null : Estado.Trim();
        Area = string.IsNullOrWhiteSpace(Area) ? null : Area.Trim();
        Pagina = Pagina < 1 ? 1 : Pagina;
        TamanoPagina = TamanoPagina is < 1 or > 100 ? 8 : TamanoPagina;
    }
}

public class FiltroMovimientos
{
    public string? Texto { get; set; }
    public string? Entidad { get; set; }
    public string? Accion { get; set; }
    public int Pagina { get; set; } = 1;
    public int TamanoPagina { get; set; } = 15;

    public void Normalizar()
    {
        Texto = string.IsNullOrWhiteSpace(Texto) ? null : Texto.Trim();
        Entidad = string.IsNullOrWhiteSpace(Entidad) ? null : Entidad.Trim();
        Accion = string.IsNullOrWhiteSpace(Accion) ? null : Accion.Trim();
        Pagina = Pagina < 1 ? 1 : Pagina;
        TamanoPagina = TamanoPagina is < 1 or > 100 ? 15 : TamanoPagina;
    }
}
