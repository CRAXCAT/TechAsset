using TechAsset.Application.DTOs;
using TechAsset.Application.Models;
using TechAsset.Domain.Entities;

namespace TechAsset.Application.Interfaces;

public interface IEquipoRepository
{
    Task<IReadOnlyList<Equipo>> ListarAsync(FiltroEquipos filtro);
    Task<IReadOnlyList<Equipo>> ObtenerTodosAsync();
    Task<Equipo?> ObtenerPorIdAsync(Guid id);
    Task<bool> ExisteCodigoAsync(string codigo, Guid? excluirId = null);
    Task<bool> TienePrestamosAsync(Guid equipoId);
    Task AgregarAsync(Equipo equipo);
    Task ActualizarAsync(Equipo equipo);
    Task EliminarAsync(Equipo equipo);
}

public interface IEquipoService
{
    Task<IReadOnlyList<EquipoDto>> ListarAsync(FiltroEquipos filtro);
    Task<IReadOnlyList<EquipoDto>> ObtenerTodosAsync();
    Task<EquipoDto> ObtenerPorIdAsync(Guid id);
    Task<EquipoDto> CrearAsync(CrearEquipoDto dto);
    Task<EquipoDto> ActualizarAsync(Guid id, CrearEquipoDto dto);
    Task<EquipoDto> CambiarEstadoAsync(Guid id, string estado);
    Task EliminarAsync(Guid id);
}
