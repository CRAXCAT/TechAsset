using System.Security.Claims;
using TechAsset.Application.DTOs;
using TechAsset.Application.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace TechAsset.API.Controllers;

/// <summary>
/// Autenticación con correo institucional y contraseña. Devuelve un token JWT
/// que el frontend envía en la cabecera Authorization.
/// </summary>
[ApiController]
[Route("api/auth")]
[Produces("application/json")]
public class AuthController : ControllerBase
{
    private readonly IAuthService authService;

    public AuthController(IAuthService authService)
    {
        this.authService = authService;
    }

    /// <summary>
    /// Inicia sesión y devuelve el token, el usuario y si debe cambiar la clave.
    /// </summary>
    [HttpPost("login")]
    [AllowAnonymous]
    [ProducesResponseType(typeof(SesionDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<ActionResult<SesionDto>> Login([FromBody] LoginDto dto)
        => Ok(await authService.LoginAsync(dto));

    /// <summary>
    /// Cambia la contraseña del usuario autenticado (incluida la temporal).
    /// </summary>
    [HttpPost("cambiar-clave")]
    [Authorize]
    [ProducesResponseType(typeof(UsuarioDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    public async Task<ActionResult<UsuarioDto>> CambiarClave([FromBody] CambiarClaveDto dto)
    {
        var id = Guid.Parse(User.FindFirstValue(ClaimTypes.NameIdentifier)!);
        return Ok(await authService.CambiarClaveAsync(id, dto));
    }
}
