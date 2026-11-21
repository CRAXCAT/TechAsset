using Microsoft.EntityFrameworkCore;
using TechAsset.Application.Interfaces;
using TechAsset.Application.Models;
using TechAsset.Domain.Entities;
using TechAsset.Infrastructure.Data;

namespace TechAsset.Infrastructure.Repositories;

public class PrestamoRepository : IPrestamoRepository
{
    private readonly AppDbContext context;

    public PrestamoRepository(AppDbContext context)
    {
        this.context = context;
    }

    public async Task<(IReadOnlyList<Prestamo> Items, int Total)> ListarAsync(FiltroPrestamos filtro, Guid? usuarioId = null)
    {
        var consulta = context.Prestamos
            .AsNoTracking()
            .Include(p => p.Usuario)
            .Include(p => p.Equipo)
            .Include(p => p.Responsable)
            .AsQueryable();

        if (usuarioId is not null)
        {
            consulta = consulta.Where(p => p.UsuarioId == usuarioId);
        }

        if (!string.IsNullOrWhiteSpace(filtro.Texto))
        {
            var patron = $"%{filtro.Texto}%";
            consulta = consulta.Where(p =>
                EF.Functions.ILike(p.Equipo.Nombre, patron) ||
                EF.Functions.ILike(p.Equipo.CodigoPatrimonial, patron) ||
                EF.Functions.ILike(p.Usuario.Nombres, patron) ||
                EF.Functions.ILike(p.Usuario.Apellidos, patron));
        }

        if (!string.IsNullOrWhiteSpace(filtro.Estado))
        {
            consulta = consulta.Where(p => p.Estado == filtro.Estado);
        }

        if (!string.IsNullOrWhiteSpace(filtro.Area))
        {
            consulta = consulta.Where(p => p.Usuario.Area == filtro.Area);
        }

        if (filtro.EquipoId is not null)
        {
            consulta = consulta.Where(p => p.EquipoId == filtro.EquipoId);
        }

        if (filtro.Desde is not null)
        {
            consulta = consulta.Where(p => p.FechaPrestamo >= filtro.Desde);
        }

        if (filtro.Hasta is not null)
        {
            consulta = consulta.Where(p => p.FechaPrestamo <= filtro.Hasta);
        }

        var total = await consulta.CountAsync();

        var items = await consulta
            .OrderByDescending(p => p.Estado == "Activo")
            .ThenByDescending(p => p.FechaPrestamo)
            .ThenByDescending(p => p.FechaRegistro)
            .Skip((filtro.Pagina - 1) * filtro.TamanoPagina)
            .Take(filtro.TamanoPagina)
            .ToListAsync();

        return (items, total);
    }

    public async Task<IReadOnlyList<Prestamo>> ObtenerTodosAsync(Guid? usuarioId = null)
    {
        var consulta = context.Prestamos
            .AsNoTracking()
            .Include(p => p.Usuario)
            .Include(p => p.Equipo)
            .Include(p => p.Responsable)
            .AsQueryable();

        if (usuarioId is not null)
        {
            consulta = consulta.Where(p => p.UsuarioId == usuarioId);
        }

        return await consulta.ToListAsync();
    }

    public async Task<Prestamo?> ObtenerPorIdAsync(Guid id)
        => await context.Prestamos
            .AsNoTracking()
            .Include(p => p.Usuario)
            .Include(p => p.Equipo)
            .Include(p => p.Responsable)
            .FirstOrDefaultAsync(p => p.Id == id);

    public async Task<Prestamo?> ObtenerActivoPorEquipoAsync(Guid equipoId)
        => await context.Prestamos
            .AsNoTracking()
            .Include(p => p.Usuario)
            .Include(p => p.Equipo)
            .FirstOrDefaultAsync(p => p.EquipoId == equipoId && p.Estado == "Activo");

    public async Task AgregarAsync(Prestamo prestamo)
    {
        context.Prestamos.Add(prestamo);
        await context.SaveChangesAsync();
    }

    public async Task ActualizarAsync(Prestamo prestamo)
    {
        var existente = await context.Prestamos.FirstOrDefaultAsync(p => p.Id == prestamo.Id);
        if (existente is null)
        {
            return;
        }

        context.Entry(existente).CurrentValues.SetValues(prestamo);
        await context.SaveChangesAsync();
    }
}
