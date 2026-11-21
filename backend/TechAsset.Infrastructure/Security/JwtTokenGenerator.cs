using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Tokens;
using TechAsset.Application.Interfaces;
using TechAsset.Domain.Entities;

namespace TechAsset.Infrastructure.Security;

/// <summary>
/// Genera tokens JWT firmados con HMAC-SHA256. El token incluye el id, el
/// nombre, el correo y el rol del usuario, y expira según la configuración.
/// </summary>
public class JwtTokenGenerator : ITokenGenerator
{
    private readonly IConfiguration configuration;

    public JwtTokenGenerator(IConfiguration configuration)
    {
        this.configuration = configuration;
    }

    public (string Token, DateTime ExpiraUtc) Generar(Usuario usuario)
    {
        var clave = configuration["Jwt:Key"] ?? throw new InvalidOperationException("Falta configurar Jwt:Key.");
        var emisor = configuration["Jwt:Issuer"] ?? "TechAsset";
        var audiencia = configuration["Jwt:Audience"] ?? "TechAsset.Web";
        var minutos = int.TryParse(configuration["Jwt:ExpiraMinutos"], out var valor) ? valor : 480;
        var expira = DateTime.UtcNow.AddMinutes(minutos);

        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, usuario.Id.ToString()),
            new Claim(ClaimTypes.NameIdentifier, usuario.Id.ToString()),
            new Claim(ClaimTypes.Name, $"{usuario.Nombres} {usuario.Apellidos}".Trim()),
            new Claim(ClaimTypes.Email, usuario.Correo),
            new Claim(ClaimTypes.Role, usuario.Rol),
            new Claim("debeCambiarPassword", usuario.DebeCambiarPassword.ToString().ToLowerInvariant())
        };

        var credenciales = new SigningCredentials(
            new SymmetricSecurityKey(Encoding.UTF8.GetBytes(clave)),
            SecurityAlgorithms.HmacSha256);

        var descriptor = new JwtSecurityToken(
            issuer: emisor,
            audience: audiencia,
            claims: claims,
            notBefore: DateTime.UtcNow,
            expires: expira,
            signingCredentials: credenciales);

        return (new JwtSecurityTokenHandler().WriteToken(descriptor), expira);
    }
}
