using TechAsset.Application.DTOs;
using TechAsset.Application.Models;
using TechAsset.Domain.Entities;

namespace TechAsset.Application.Interfaces;

public interface IMovimientoRepository
{
    Task<(IReadOnlyList<Movimiento> Items, int Total)> ListarAsync(FiltroMovimientos filtro);
    Task AgregarAsync(Movimiento movimiento);
}

public interface IMovimientoService
{
    Task<ResultadoPaginado<MovimientoDto>> ListarAsync(FiltroMovimientos filtro);
    Task RegistrarAsync(
        string entidad,
        Guid entidadId,
        string accion,
        string detalle,
        Guid? usuarioId,
        string usuarioNombre);
}
