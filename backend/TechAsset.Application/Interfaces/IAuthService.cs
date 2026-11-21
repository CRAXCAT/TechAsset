using TechAsset.Application.DTOs;

namespace TechAsset.Application.Interfaces;

/// <summary>
/// Contrato del servicio de hash. Infrastructure decide el algoritmo
/// (BCrypt) sin que Application conozca los detalles.
/// </summary>
public interface IPasswordHasher
{
    string Hashear(string clave);
    bool Verificar(string clave, string hash);
}

public interface IAuthService
{
    Task<SesionDto> LoginAsync(LoginDto dto);
    Task<UsuarioDto> CambiarClaveAsync(Guid usuarioId, CambiarClaveDto dto);
}
