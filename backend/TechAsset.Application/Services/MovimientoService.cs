using TechAsset.Application.DTOs;
using TechAsset.Application.Interfaces;
using TechAsset.Application.Models;
using TechAsset.Domain.Entities;

namespace TechAsset.Application.Services;

public class MovimientoService : IMovimientoService
{
    private readonly IMovimientoRepository movimientoRepository;

    public MovimientoService(IMovimientoRepository movimientoRepository)
    {
        this.movimientoRepository = movimientoRepository;
    }

    public async Task<ResultadoPaginado<MovimientoDto>> ListarAsync(FiltroMovimientos filtro)
    {
        filtro ??= new FiltroMovimientos();
        filtro.Normalizar();
        var (items, total) = await movimientoRepository.ListarAsync(filtro);

        return new ResultadoPaginado<MovimientoDto>
        {
            Items = items.Select(Mapear).ToList(),
            Total = total,
            Pagina = filtro.Pagina,
            TamanoPagina = filtro.TamanoPagina
        };
    }

    public async Task RegistrarAsync(
        string entidad,
        Guid entidadId,
        string accion,
        string detalle,
        Guid? usuarioId,
        string usuarioNombre)
    {
        await movimientoRepository.AgregarAsync(new Movimiento
        {
            Id = Guid.NewGuid(),
            Fecha = DateTime.UtcNow,
            Entidad = entidad,
            EntidadId = entidadId,
            Accion = accion,
            Detalle = detalle.Length > 300 ? detalle[..300] : detalle,
            UsuarioId = usuarioId,
            UsuarioNombre = usuarioNombre
        });
    }

    private static MovimientoDto Mapear(Movimiento movimiento) => new()
    {
        Id = movimiento.Id,
        Fecha = movimiento.Fecha,
        Entidad = movimiento.Entidad,
        EntidadId = movimiento.EntidadId,
        Accion = movimiento.Accion,
        Detalle = movimiento.Detalle,
        UsuarioId = movimiento.UsuarioId,
        UsuarioNombre = movimiento.UsuarioNombre
    };
}
