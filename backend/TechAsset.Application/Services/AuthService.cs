using TechAsset.Application.DTOs;
using TechAsset.Application.Exceptions;
using TechAsset.Application.Interfaces;
using TechAsset.Domain.Entities;

namespace TechAsset.Application.Services;

public class AuthService : IAuthService
{
    private readonly IUsuarioRepository usuarioRepository;
    private readonly IPasswordHasher passwordHasher;
    private readonly ITokenGenerator tokenGenerator;

    public AuthService(
        IUsuarioRepository usuarioRepository,
        IPasswordHasher passwordHasher,
        ITokenGenerator tokenGenerator)
    {
        this.usuarioRepository = usuarioRepository;
        this.passwordHasher = passwordHasher;
        this.tokenGenerator = tokenGenerator;
    }

    public async Task<SesionDto> LoginAsync(LoginDto dto)
    {
        var correo = (dto.Correo ?? string.Empty).Trim().ToLowerInvariant();
        var clave = dto.Clave ?? string.Empty;

        if (string.IsNullOrWhiteSpace(correo) || string.IsNullOrWhiteSpace(clave))
        {
            throw new CredencialesInvalidasException();
        }

        var usuario = await usuarioRepository.ObtenerPorCorreoAsync(correo);

        // Mismo mensaje para correo inexistente, clave incorrecta o cuenta inactiva:
        // así no se revela qué dato falló ni si la cuenta existe.
        if (usuario is null || !usuario.Activo || !passwordHasher.Verificar(clave, usuario.PasswordHash))
        {
            throw new CredencialesInvalidasException();
        }

        var (token, expira) = tokenGenerator.Generar(usuario);

        return new SesionDto
        {
            Token = token,
            Usuario = Mapear(usuario),
            ExpiraUtc = expira
        };
    }

    public async Task<UsuarioDto> CambiarClaveAsync(Guid usuarioId, CambiarClaveDto dto)
    {
        var usuario = await usuarioRepository.ObtenerPorIdAsync(usuarioId)
            ?? throw new RecursoNoEncontradoException("No se encontró la cuenta solicitada.");

        var actual = dto.ClaveActual ?? string.Empty;
        var nueva = dto.ClaveNueva ?? string.Empty;

        if (!passwordHasher.Verificar(actual, usuario.PasswordHash))
        {
            throw new ReglaNegocioException("La contraseña actual no es correcta.");
        }

        if (nueva == actual)
        {
            throw new ReglaNegocioException("La nueva contraseña debe ser diferente de la actual.");
        }

        if (!EsClaveSegura(nueva))
        {
            throw new ReglaNegocioException(
                "La nueva contraseña debe tener al menos 8 caracteres e incluir mayúscula, minúscula, número y símbolo.");
        }

        usuario.PasswordHash = passwordHasher.Hashear(nueva);
        usuario.DebeCambiarPassword = false;
        await usuarioRepository.ActualizarAsync(usuario);

        return Mapear(usuario);
    }

    public static bool EsClaveSegura(string clave)
        => clave.Length >= 8
           && clave.Any(char.IsUpper)
           && clave.Any(char.IsLower)
           && clave.Any(char.IsDigit)
           && clave.Any(c => !char.IsLetterOrDigit(c));

    public static UsuarioDto Mapear(Usuario usuario) => new()
    {
        Id = usuario.Id,
        Nombres = usuario.Nombres,
        Apellidos = usuario.Apellidos,
        NombreCompleto = $"{usuario.Nombres} {usuario.Apellidos}".Trim(),
        Correo = usuario.Correo,
        Area = usuario.Area,
        Rol = usuario.Rol,
        Activo = usuario.Activo,
        DebeCambiarPassword = usuario.DebeCambiarPassword,
        FechaRegistro = usuario.FechaRegistro
    };
}
