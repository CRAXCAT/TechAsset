using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using TechAsset.Application.DTOs;
using TechAsset.Application.Interfaces;
using TechAsset.Application.Models;

namespace TechAsset.API.Controllers;

[ApiController]
[Route("api/movimientos")]
[Produces("application/json")]
[Authorize(Roles = "Administrador,Responsable")]
public class MovimientosController : ControllerBase
{
    private readonly IMovimientoService movimientoService;

    public MovimientosController(IMovimientoService movimientoService)
    {
        this.movimientoService = movimientoService;
    }

    /// <summary>Consulta la auditoría de operaciones del sistema.</summary>
    [HttpGet]
    public async Task<ActionResult<ResultadoPaginado<MovimientoDto>>> Listar([FromQuery] FiltroMovimientos filtro)
        => Ok(await movimientoService.ListarAsync(filtro));
}
