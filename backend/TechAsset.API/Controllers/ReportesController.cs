using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using TechAsset.Application.DTOs;
using TechAsset.Application.Interfaces;
using TechAsset.Application.Models;

namespace TechAsset.API.Controllers;

[ApiController]
[Route("api/reportes")]
[Produces("application/json")]
[Authorize]
public class ReportesController : ControllerBase
{
    private readonly IReporteService reporteService;

    public ReportesController(IReporteService reporteService)
    {
        this.reporteService = reporteService;
    }

    /// <summary>Indicadores del dashboard y reportes agregados; el Colaborador ve solo sus préstamos.</summary>
    [HttpGet("resumen")]
    public async Task<ActionResult<ResumenTechAssetDto>> Resumen()
        => Ok(await reporteService.ObtenerResumenAsync(UsuarioId(), EsGestor()));

    /// <summary>Exporta el historial de préstamos filtrado en CSV.</summary>
    [HttpGet("prestamos.csv")]
    [Authorize(Roles = "Administrador,Responsable")]
    public async Task<IActionResult> ExportarPrestamos([FromQuery] FiltroPrestamos filtro)
    {
        var contenido = await reporteService.ExportarPrestamosCsvAsync(filtro, UsuarioId(), EsGestor());
        return File(contenido, "text/csv", "prestamos-techasset.csv");
    }

    /// <summary>Exporta el inventario filtrado en CSV.</summary>
    [HttpGet("equipos.csv")]
    [Authorize(Roles = "Administrador,Responsable")]
    public async Task<IActionResult> ExportarEquipos([FromQuery] FiltroEquipos filtro)
    {
        var contenido = await reporteService.ExportarEquiposCsvAsync(filtro);
        return File(contenido, "text/csv", "inventario-techasset.csv");
    }

    private Guid UsuarioId() => Guid.Parse(User.FindFirstValue(ClaimTypes.NameIdentifier)!);

    private bool EsGestor() => User.IsInRole("Administrador") || User.IsInRole("Responsable");
}
