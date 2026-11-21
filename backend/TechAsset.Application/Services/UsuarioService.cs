using TechAsset.Application.DTOs;
using TechAsset.Application.Exceptions;
using TechAsset.Application.Interfaces;
using TechAsset.Application.Models;
using TechAsset.Domain.Constantes;
using TechAsset.Domain.Entities;

namespace TechAsset.Application.Services;

public class UsuarioService : IUsuarioService
{
    private readonly IUsuarioRepository usuarioRepository;
    private readonly IPasswordHasher passwordHasher;

    public UsuarioService(IUsuarioRepository usuarioRepository, IPasswordHasher passwordHasher)
    {
        this.usuarioRepository = usuarioRepository;
        this.passwordHasher = passwordHasher;
    }

    public async Task<IReadOnlyList<UsuarioDto>> ListarAsync(FiltroUsuarios filtro)
    {
        filtro ??= new FiltroUsuarios();
        filtro.Normalizar();

        if (filtro.Area is not null && !CatalogoTechAsset.EsAreaValida(filtro.Area))
        {
            throw new ReglaNegocioException("El área solicitada no es válida.");
        }

        if (filtro.Rol is not null && !CatalogoTechAsset.EsRolValido(filtro.Rol))
        {
            throw new ReglaNegocioException("El rol solicitado no es válido.");
        }

        var usuarios = await usuarioRepository.ListarAsync(filtro);
        return usuarios.Select(Mapear).ToList();
    }

    public async Task<UsuarioDto> CrearAsync(CrearUsuarioDto dto)
    {
        var nombres = Normalizar(dto.Nombres);
        var apellidos = Normalizar(dto.Apellidos);
        var correo = Normalizar(dto.Correo).ToLowerInvariant();
        var area = Normalizar(dto.Area);
        var rol = Normalizar(dto.Rol);

        ValidarCatalogos(area, rol);

        if (await usuarioRepository.ExisteCorreoAsync(correo))
        {
            throw new ReglaNegocioException("Ya existe un usuario registrado con ese correo institucional (RN-08).");
        }

        var usuario = new Usuario
        {
            Id = Guid.NewGuid(),
            Nombres = nombres,
            Apellidos = apellidos,
            Correo = correo,
            Area = area,
            Rol = rol,
            Activo = true,
            PasswordHash = passwordHasher.Hashear(dto.ClaveTemporal ?? string.Empty),
            DebeCambiarPassword = true,
            FechaRegistro = DateTime.UtcNow
        };

        await usuarioRepository.AgregarAsync(usuario);
        return Mapear(usuario);
    }

    public async Task<UsuarioDto> ActualizarAsync(Guid id, ActualizarUsuarioDto dto)
    {
        var usuario = await usuarioRepository.ObtenerPorIdAsync(id)
            ?? throw new RecursoNoEncontradoException("No se encontró el usuario solicitado.");

        var nombres = Normalizar(dto.Nombres);
        var apellidos = Normalizar(dto.Apellidos);
        var correo = Normalizar(dto.Correo).ToLowerInvariant();
        var area = Normalizar(dto.Area);
        var rol = Normalizar(dto.Rol);

        ValidarCatalogos(area, rol);

        if (await usuarioRepository.ExisteCorreoAsync(correo, id))
        {
            throw new ReglaNegocioException("Ya existe otro usuario con ese correo institucional (RN-08).");
        }

        usuario.Nombres = nombres;
        usuario.Apellidos = apellidos;
        usuario.Correo = correo;
        usuario.Area = area;
        usuario.Rol = rol;

        await usuarioRepository.ActualizarAsync(usuario);
        return Mapear(usuario);
    }

    public async Task<UsuarioDto> CambiarActivoAsync(Guid id, bool activo)
    {
        var usuario = await usuarioRepository.ObtenerPorIdAsync(id)
            ?? throw new RecursoNoEncontradoException("No se encontró el usuario solicitado.");

        if (!activo && await usuarioRepository.TienePrestamosActivosAsync(id))
        {
            throw new ReglaNegocioException("No se puede deshabilitar el usuario porque tiene préstamos activos.");
        }

        usuario.Activo = activo;
        await usuarioRepository.ActualizarAsync(usuario);
        return Mapear(usuario);
    }

    private static void ValidarCatalogos(string area, string rol)
    {
        if (!CatalogoTechAsset.EsAreaValida(area))
        {
            throw new ReglaNegocioException("El área seleccionada no es válida.");
        }

        if (!CatalogoTechAsset.EsRolValido(rol))
        {
            throw new ReglaNegocioException("El rol seleccionado no es válido.");
        }
    }

    private static string Normalizar(string? valor)
        => string.IsNullOrWhiteSpace(valor)
            ? string.Empty
            : string.Join(' ', valor.Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries));

    public static UsuarioDto Mapear(Usuario usuario) => new()
    {
        Id = usuario.Id,
        Nombres = usuario.Nombres,
        Apellidos = usuario.Apellidos,
        NombreCompleto = $"{usuario.Nombres} {usuario.Apellidos}".Trim(),
        Correo = usuario.Correo,
        Area = usuario.Area,
        Rol = usuario.Rol,
        Activo = usuario.Activo,
        DebeCambiarPassword = usuario.DebeCambiarPassword,
        FechaRegistro = usuario.FechaRegistro
    };
}
