using TechAsset.Application.DTOs;
using TechAsset.Application.Interfaces;
using TechAsset.Application.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace TechAsset.API.Controllers;

[ApiController]
[Route("api/usuarios")]
[Produces("application/json")]
[Authorize]
public class UsuariosController : ControllerBase
{
    private readonly IUsuarioService usuarioService;

    public UsuariosController(IUsuarioService usuarioService)
    {
        this.usuarioService = usuarioService;
    }

    /// <summary>Lista usuarios con búsqueda, área, rol y estado.</summary>
    [HttpGet]
    [Authorize(Roles = "Administrador,Responsable")]
    public async Task<ActionResult<IReadOnlyList<UsuarioDto>>> Listar([FromQuery] FiltroUsuarios filtro)
        => Ok(await usuarioService.ListarAsync(filtro));

    /// <summary>Registra un colaborador con contraseña temporal.</summary>
    [HttpPost]
    [Authorize(Roles = "Administrador")]
    public async Task<ActionResult<UsuarioDto>> Crear([FromBody] CrearUsuarioDto dto)
    {
        var usuario = await usuarioService.CrearAsync(dto);
        return StatusCode(StatusCodes.Status201Created, usuario);
    }

    /// <summary>Actualiza nombres, correo, área y rol.</summary>
    [HttpPut("{id:guid}")]
    [Authorize(Roles = "Administrador")]
    public async Task<ActionResult<UsuarioDto>> Actualizar(Guid id, [FromBody] ActualizarUsuarioDto dto)
        => Ok(await usuarioService.ActualizarAsync(id, dto));

    /// <summary>Habilita o deshabilita una cuenta (solo Administrador, RN-09).</summary>
    [HttpPatch("{id:guid}/activo")]
    [Authorize(Roles = "Administrador")]
    public async Task<ActionResult<UsuarioDto>> CambiarActivo(Guid id, [FromQuery] bool activo)
        => Ok(await usuarioService.CambiarActivoAsync(id, activo));
}
