namespace TechAsset.Application.DTOs;

public class LoginDto
{
    public string Correo { get; set; } = string.Empty;
    public string Clave { get; set; } = string.Empty;
}

public class SesionDto
{
    public string Token { get; set; } = string.Empty;
    public UsuarioDto Usuario { get; set; } = new();
    public DateTime ExpiraUtc { get; set; }
}

public class CambiarClaveDto
{
    public string ClaveActual { get; set; } = string.Empty;
    public string ClaveNueva { get; set; } = string.Empty;
}
