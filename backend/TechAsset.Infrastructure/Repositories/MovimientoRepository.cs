using Microsoft.EntityFrameworkCore;
using TechAsset.Application.Interfaces;
using TechAsset.Application.Models;
using TechAsset.Domain.Entities;
using TechAsset.Infrastructure.Data;

namespace TechAsset.Infrastructure.Repositories;

public class MovimientoRepository : IMovimientoRepository
{
    private readonly AppDbContext context;

    public MovimientoRepository(AppDbContext context)
    {
        this.context = context;
    }

    public async Task<(IReadOnlyList<Movimiento> Items, int Total)> ListarAsync(FiltroMovimientos filtro)
    {
        var consulta = context.Movimientos.AsNoTracking().AsQueryable();

        if (!string.IsNullOrWhiteSpace(filtro.Texto))
        {
            var patron = $"%{filtro.Texto}%";
            consulta = consulta.Where(m =>
                EF.Functions.ILike(m.Detalle, patron) ||
                EF.Functions.ILike(m.UsuarioNombre, patron) ||
                EF.Functions.ILike(m.Entidad, patron) ||
                EF.Functions.ILike(m.Accion, patron));
        }

        if (!string.IsNullOrWhiteSpace(filtro.Entidad))
        {
            consulta = consulta.Where(m => m.Entidad == filtro.Entidad);
        }

        if (!string.IsNullOrWhiteSpace(filtro.Accion))
        {
            consulta = consulta.Where(m => m.Accion == filtro.Accion);
        }

        var total = await consulta.CountAsync();
        var items = await consulta
            .OrderByDescending(m => m.Fecha)
            .Skip((filtro.Pagina - 1) * filtro.TamanoPagina)
            .Take(filtro.TamanoPagina)
            .ToListAsync();

        return (items, total);
    }

    public async Task AgregarAsync(Movimiento movimiento)
    {
        context.Movimientos.Add(movimiento);
        await context.SaveChangesAsync();
    }
}
