using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using TechAsset.Application.DTOs;
using TechAsset.Application.Interfaces;
using TechAsset.Application.Models;

namespace TechAsset.API.Controllers;

[ApiController]
[Route("api/prestamos")]
[Produces("application/json")]
[Authorize]
public class PrestamosController : ControllerBase
{
    private readonly IPrestamoService prestamoService;

    public PrestamosController(IPrestamoService prestamoService)
    {
        this.prestamoService = prestamoService;
    }

    /// <summary>Historial y préstamos activos con filtros, búsqueda y paginación.</summary>
    [HttpGet]
    public async Task<ActionResult<ResultadoPaginado<PrestamoDto>>> Listar([FromQuery] FiltroPrestamos filtro)
        => Ok(await prestamoService.ListarAsync(filtro, UsuarioId(), EsGestor()));

    /// <summary>Consulta el detalle de un préstamo.</summary>
    [HttpGet("{id:guid}")]
    public async Task<ActionResult<PrestamoDto>> Obtener(Guid id)
        => Ok(await prestamoService.ObtenerPorIdAsync(id, UsuarioId(), EsGestor()));

    /// <summary>Registra un préstamo (Responsable de Tecnología o Administrador).</summary>
    [HttpPost]
    [Authorize(Roles = "Administrador,Responsable")]
    public async Task<ActionResult<PrestamoDto>> Crear([FromBody] CrearPrestamoDto dto)
    {
        var prestamo = await prestamoService.CrearAsync(dto, UsuarioId());
        return StatusCode(StatusCodes.Status201Created, prestamo);
    }

    /// <summary>Registra la devolución con observaciones (RN-10).</summary>
    [HttpPatch("{id:guid}/devolver")]
    [Authorize(Roles = "Administrador,Responsable")]
    public async Task<ActionResult<PrestamoDto>> Devolver(Guid id, [FromBody] DevolverPrestamoDto dto)
        => Ok(await prestamoService.DevolverAsync(id, dto.ObservacionDevolucion, UsuarioId()));

    private Guid UsuarioId() => Guid.Parse(User.FindFirstValue(ClaimTypes.NameIdentifier)!);

    private bool EsGestor() => User.IsInRole("Administrador") || User.IsInRole("Responsable");
}
