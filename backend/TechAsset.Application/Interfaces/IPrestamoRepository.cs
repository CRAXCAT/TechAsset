using TechAsset.Application.DTOs;
using TechAsset.Application.Models;
using TechAsset.Domain.Entities;

namespace TechAsset.Application.Interfaces;

public interface IPrestamoRepository
{
    Task<(IReadOnlyList<Prestamo> Items, int Total)> ListarAsync(FiltroPrestamos filtro, Guid? usuarioId = null);
    Task<IReadOnlyList<Prestamo>> ObtenerTodosAsync(Guid? usuarioId = null);
    Task<Prestamo?> ObtenerPorIdAsync(Guid id);
    Task<Prestamo?> ObtenerActivoPorEquipoAsync(Guid equipoId);
    Task AgregarAsync(Prestamo prestamo);
    Task ActualizarAsync(Prestamo prestamo);
}

public interface IPrestamoService
{
    Task<ResultadoPaginado<PrestamoDto>> ListarAsync(FiltroPrestamos filtro, Guid? usuarioId, bool esGestor);
    Task<PrestamoDto> ObtenerPorIdAsync(Guid id, Guid? usuarioId, bool esGestor);
    Task<PrestamoDto> CrearAsync(CrearPrestamoDto dto, Guid responsableId);
    Task<PrestamoDto> DevolverAsync(Guid id, string observacion, Guid usuarioId);
    Task<ResumenTechAssetDto> ObtenerResumenAsync(Guid? usuarioId, bool esGestor);
}

public interface IReporteService
{
    Task<ResumenTechAssetDto> ObtenerResumenAsync(Guid? usuarioId, bool esGestor);
    Task<byte[]> ExportarPrestamosCsvAsync(FiltroPrestamos filtro, Guid? usuarioId, bool esGestor);
    Task<byte[]> ExportarEquiposCsvAsync(FiltroEquipos filtro);
}
