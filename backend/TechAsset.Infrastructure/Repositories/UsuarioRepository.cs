using Microsoft.EntityFrameworkCore;
using TechAsset.Application.Interfaces;
using TechAsset.Application.Models;
using TechAsset.Domain.Entities;
using TechAsset.Infrastructure.Data;

namespace TechAsset.Infrastructure.Repositories;

public class UsuarioRepository : IUsuarioRepository
{
    private readonly AppDbContext context;

    public UsuarioRepository(AppDbContext context)
    {
        this.context = context;
    }

    public async Task<IReadOnlyList<Usuario>> ListarAsync(FiltroUsuarios filtro)
    {
        var consulta = context.Usuarios.AsNoTracking().AsQueryable();

        if (!string.IsNullOrWhiteSpace(filtro.Texto))
        {
            var patron = $"%{filtro.Texto}%";
            consulta = consulta.Where(u =>
                EF.Functions.ILike(u.Nombres, patron) ||
                EF.Functions.ILike(u.Apellidos, patron) ||
                EF.Functions.ILike(u.Correo, patron));
        }

        if (!string.IsNullOrWhiteSpace(filtro.Area))
        {
            consulta = consulta.Where(u => u.Area == filtro.Area);
        }

        if (!string.IsNullOrWhiteSpace(filtro.Rol))
        {
            consulta = consulta.Where(u => u.Rol == filtro.Rol);
        }

        if (filtro.Activo is not null)
        {
            consulta = consulta.Where(u => u.Activo == filtro.Activo);
        }

        return await consulta.OrderBy(u => u.Apellidos).ThenBy(u => u.Nombres).ToListAsync();
    }

    public async Task<IReadOnlyList<Usuario>> ObtenerTodosAsync()
        => await context.Usuarios.AsNoTracking().OrderBy(u => u.Apellidos).ToListAsync();

    public async Task<Usuario?> ObtenerPorIdAsync(Guid id)
        => await context.Usuarios.AsNoTracking().FirstOrDefaultAsync(u => u.Id == id);

    public async Task<Usuario?> ObtenerPorCorreoAsync(string correo)
        => await context.Usuarios.AsNoTracking().FirstOrDefaultAsync(u => EF.Functions.ILike(u.Correo, correo));

    public async Task<bool> ExisteCorreoAsync(string correo, Guid? excluirId = null)
        => await context.Usuarios.AnyAsync(u =>
            EF.Functions.ILike(u.Correo, correo) && (excluirId == null || u.Id != excluirId));

    public async Task<bool> TienePrestamosActivosAsync(Guid usuarioId)
        => await context.Prestamos.AnyAsync(p => p.UsuarioId == usuarioId && p.Estado == "Activo");

    public async Task AgregarAsync(Usuario usuario)
    {
        context.Usuarios.Add(usuario);
        await context.SaveChangesAsync();
    }

    public async Task ActualizarAsync(Usuario usuario)
    {
        context.Usuarios.Update(usuario);
        await context.SaveChangesAsync();
    }
}
