using Microsoft.EntityFrameworkCore;
using TechAsset.Application.Interfaces;
using TechAsset.Application.Models;
using TechAsset.Domain.Entities;
using TechAsset.Infrastructure.Data;

namespace TechAsset.Infrastructure.Repositories;

public class EquipoRepository : IEquipoRepository
{
    private readonly AppDbContext context;

    public EquipoRepository(AppDbContext context)
    {
        this.context = context;
    }

    public async Task<IReadOnlyList<Equipo>> ListarAsync(FiltroEquipos filtro)
    {
        var consulta = context.Equipos.AsNoTracking().Include(e => e.Prestamos).AsQueryable();

        if (!string.IsNullOrWhiteSpace(filtro.Texto))
        {
            var patron = $"%{filtro.Texto}%";
            consulta = consulta.Where(e =>
                EF.Functions.ILike(e.Nombre, patron) ||
                EF.Functions.ILike(e.CodigoPatrimonial, patron) ||
                EF.Functions.ILike(e.Marca, patron));
        }

        if (!string.IsNullOrWhiteSpace(filtro.Categoria))
        {
            consulta = consulta.Where(e => e.Categoria == filtro.Categoria);
        }

        if (!string.IsNullOrWhiteSpace(filtro.Estado))
        {
            consulta = consulta.Where(e => e.Estado == filtro.Estado);
        }

        return await consulta.OrderBy(e => e.CodigoPatrimonial).ToListAsync();
    }

    public async Task<IReadOnlyList<Equipo>> ObtenerTodosAsync()
        => await context.Equipos.AsNoTracking().Include(e => e.Prestamos).OrderBy(e => e.CodigoPatrimonial).ToListAsync();

    public async Task<Equipo?> ObtenerPorIdAsync(Guid id)
        => await context.Equipos.AsNoTracking().Include(e => e.Prestamos).FirstOrDefaultAsync(e => e.Id == id);

    public async Task<bool> ExisteCodigoAsync(string codigo, Guid? excluirId = null)
        => await context.Equipos.AnyAsync(e =>
            EF.Functions.ILike(e.CodigoPatrimonial, codigo) && (excluirId == null || e.Id != excluirId));

    public async Task<bool> TienePrestamosAsync(Guid equipoId)
        => await context.Prestamos.AnyAsync(p => p.EquipoId == equipoId);

    public async Task AgregarAsync(Equipo equipo)
    {
        context.Equipos.Add(equipo);
        await context.SaveChangesAsync();
    }

    public async Task ActualizarAsync(Equipo equipo)
    {
        var existente = await context.Equipos.FirstOrDefaultAsync(e => e.Id == equipo.Id);
        if (existente is null)
        {
            return;
        }

        context.Entry(existente).CurrentValues.SetValues(equipo);
        await context.SaveChangesAsync();
    }

    public async Task EliminarAsync(Equipo equipo)
    {
        context.Equipos.Remove(equipo);
        await context.SaveChangesAsync();
    }
}
