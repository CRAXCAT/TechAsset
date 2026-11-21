using TechAsset.Application.DTOs;
using TechAsset.Application.Models;
using TechAsset.Domain.Entities;

namespace TechAsset.Application.Interfaces;

public interface IUsuarioRepository
{
    Task<IReadOnlyList<Usuario>> ListarAsync(FiltroUsuarios filtro);
    Task<IReadOnlyList<Usuario>> ObtenerTodosAsync();
    Task<Usuario?> ObtenerPorIdAsync(Guid id);
    Task<Usuario?> ObtenerPorCorreoAsync(string correo);
    Task<bool> ExisteCorreoAsync(string correo, Guid? excluirId = null);
    Task<bool> TienePrestamosActivosAsync(Guid usuarioId);
    Task AgregarAsync(Usuario usuario);
    Task ActualizarAsync(Usuario usuario);
}

public interface IUsuarioService
{
    Task<IReadOnlyList<UsuarioDto>> ListarAsync(FiltroUsuarios filtro);
    Task<UsuarioDto> CrearAsync(CrearUsuarioDto dto);
    Task<UsuarioDto> ActualizarAsync(Guid id, ActualizarUsuarioDto dto);
    Task<UsuarioDto> CambiarActivoAsync(Guid id, bool activo);
}
