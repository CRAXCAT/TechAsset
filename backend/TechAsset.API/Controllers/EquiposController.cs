using TechAsset.Application.DTOs;
using TechAsset.Application.Interfaces;
using TechAsset.Application.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace TechAsset.API.Controllers;

[ApiController]
[Route("api/equipos")]
[Produces("application/json")]
[Authorize]
public class EquiposController : ControllerBase
{
    private readonly IEquipoService equipoService;

    public EquiposController(IEquipoService equipoService)
    {
        this.equipoService = equipoService;
    }

    /// <summary>Consulta el inventario con búsqueda, categoría y estado.</summary>
    [HttpGet]
    public async Task<ActionResult<IReadOnlyList<EquipoDto>>> Listar([FromQuery] FiltroEquipos filtro)
        => Ok(await equipoService.ListarAsync(filtro));

    /// <summary>Consulta el detalle de un equipo.</summary>
    [HttpGet("{id:guid}")]
    public async Task<ActionResult<EquipoDto>> ObtenerPorId(Guid id)
        => Ok(await equipoService.ObtenerPorIdAsync(id));

    /// <summary>Devuelve todos los equipos para selectores y reportes.</summary>
    [HttpGet("todos")]
    public async Task<ActionResult<IReadOnlyList<EquipoDto>>> ObtenerTodos()
        => Ok(await equipoService.ObtenerTodosAsync());

    /// <summary>Registra un equipo (Administrador o Responsable).</summary>
    [HttpPost]
    [Authorize(Roles = "Administrador,Responsable")]
    public async Task<ActionResult<EquipoDto>> Crear([FromBody] CrearEquipoDto dto)
    {
        var equipo = await equipoService.CrearAsync(dto);
        return StatusCode(StatusCodes.Status201Created, equipo);
    }

    /// <summary>Actualiza los datos de un equipo.</summary>
    [HttpPut("{id:guid}")]
    [Authorize(Roles = "Administrador,Responsable")]
    public async Task<ActionResult<EquipoDto>> Actualizar(Guid id, [FromBody] CrearEquipoDto dto)
        => Ok(await equipoService.ActualizarAsync(id, dto));

    /// <summary>Cambia el estado operativo del equipo.</summary>
    [HttpPatch("{id:guid}/estado")]
    [Authorize(Roles = "Administrador,Responsable")]
    public async Task<ActionResult<EquipoDto>> CambiarEstado(Guid id, [FromBody] CambiarEstadoEquipoDto dto)
        => Ok(await equipoService.CambiarEstadoAsync(id, dto.Estado));

    /// <summary>Elimina un equipo sin historial de préstamos (RN-06).</summary>
    [HttpDelete("{id:guid}")]
    [Authorize(Roles = "Administrador")]
    public async Task<IActionResult> Eliminar(Guid id)
    {
        await equipoService.EliminarAsync(id);
        return NoContent();
    }
}
