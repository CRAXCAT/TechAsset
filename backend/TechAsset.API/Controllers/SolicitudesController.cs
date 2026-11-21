using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using TechAsset.Application.DTOs;
using TechAsset.Application.Interfaces;
using TechAsset.Application.Models;

namespace TechAsset.API.Controllers;

[ApiController]
[Route("api/solicitudes")]
[Produces("application/json")]
[Authorize]
public class SolicitudesController : ControllerBase
{
    private readonly ISolicitudService solicitudService;

    public SolicitudesController(ISolicitudService solicitudService)
    {
        this.solicitudService = solicitudService;
    }

    /// <summary>Lista solicitudes; el Colaborador solo ve las propias.</summary>
    [HttpGet]
    public async Task<ActionResult<ResultadoPaginado<SolicitudDto>>> Listar([FromQuery] FiltroSolicitudes filtro)
        => Ok(await solicitudService.ListarAsync(filtro, UsuarioId(), EsGestor()));

    /// <summary>Consulta el detalle de una solicitud.</summary>
    [HttpGet("{id:guid}")]
    public async Task<ActionResult<SolicitudDto>> Obtener(Guid id)
        => Ok(await solicitudService.ObtenerPorIdAsync(id, UsuarioId(), EsGestor()));

    /// <summary>Registra una solicitud para el usuario autenticado.</summary>
    [HttpPost]
    public async Task<ActionResult<SolicitudDto>> Crear([FromBody] CrearSolicitudDto dto)
    {
        var solicitud = await solicitudService.CrearAsync(dto, UsuarioId());
        return StatusCode(StatusCodes.Status201Created, solicitud);
    }

    /// <summary>Aprueba una solicitud y genera el préstamo dentro de una transacción.</summary>
    [HttpPatch("{id:guid}/aprobar")]
    [Authorize(Roles = "Administrador,Responsable")]
    public async Task<ActionResult<SolicitudDto>> Aprobar(Guid id, [FromBody] RevisarSolicitudDto dto)
        => Ok(await solicitudService.AprobarAsync(id, dto.ObservacionRevision, UsuarioId()));

    /// <summary>Rechaza una solicitud con una observación obligatoria.</summary>
    [HttpPatch("{id:guid}/rechazar")]
    [Authorize(Roles = "Administrador,Responsable")]
    public async Task<ActionResult<SolicitudDto>> Rechazar(Guid id, [FromBody] RevisarSolicitudDto dto)
        => Ok(await solicitudService.RechazarAsync(id, dto.ObservacionRevision ?? string.Empty, UsuarioId()));

    private Guid UsuarioId() => Guid.Parse(User.FindFirstValue(ClaimTypes.NameIdentifier)!);

    private bool EsGestor() => User.IsInRole("Administrador") || User.IsInRole("Responsable");
}
