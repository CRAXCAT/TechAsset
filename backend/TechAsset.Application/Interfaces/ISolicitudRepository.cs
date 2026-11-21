using TechAsset.Application.DTOs;
using TechAsset.Application.Models;
using TechAsset.Domain.Entities;

namespace TechAsset.Application.Interfaces;

public interface ISolicitudRepository
{
    Task<(IReadOnlyList<Solicitud> Items, int Total)> ListarAsync(FiltroSolicitudes filtro, Guid? usuarioId);
    Task<IReadOnlyList<Solicitud>> ObtenerTodasAsync(Guid? usuarioId);
    Task<Solicitud?> ObtenerPorIdAsync(Guid id);
    Task<bool> ExistePendientePorEquipoAsync(Guid equipoId);
    Task<int> ContarPorEstadoAsync(string estado, Guid? usuarioId);
    Task AgregarAsync(Solicitud solicitud);
    Task ActualizarAsync(Solicitud solicitud);
}

public interface ISolicitudService
{
    Task<ResultadoPaginado<SolicitudDto>> ListarAsync(FiltroSolicitudes filtro, Guid usuarioId, bool esGestor);
    Task<SolicitudDto> ObtenerPorIdAsync(Guid id, Guid usuarioId, bool esGestor);
    Task<SolicitudDto> CrearAsync(CrearSolicitudDto dto, Guid usuarioId);
    Task<SolicitudDto> AprobarAsync(Guid id, string? observacion, Guid revisorId);
    Task<SolicitudDto> RechazarAsync(Guid id, string observacion, Guid revisorId);
}
