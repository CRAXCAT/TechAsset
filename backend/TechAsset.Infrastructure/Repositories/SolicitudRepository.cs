using Microsoft.EntityFrameworkCore;
using TechAsset.Application.Interfaces;
using TechAsset.Application.Models;
using TechAsset.Domain.Constantes;
using TechAsset.Domain.Entities;
using TechAsset.Infrastructure.Data;

namespace TechAsset.Infrastructure.Repositories;

public class SolicitudRepository : ISolicitudRepository
{
    private readonly AppDbContext context;

    public SolicitudRepository(AppDbContext context)
    {
        this.context = context;
    }

    public async Task<(IReadOnlyList<Solicitud> Items, int Total)> ListarAsync(FiltroSolicitudes filtro, Guid? usuarioId)
    {
        var consulta = ConsultaBase();

        if (usuarioId is not null)
        {
            consulta = consulta.Where(s => s.UsuarioId == usuarioId);
        }

        if (!string.IsNullOrWhiteSpace(filtro.Texto))
        {
            var patron = $"%{filtro.Texto}%";
            consulta = consulta.Where(s =>
                EF.Functions.ILike(s.Equipo.Nombre, patron) ||
                EF.Functions.ILike(s.Equipo.CodigoPatrimonial, patron) ||
                EF.Functions.ILike(s.Usuario.Nombres, patron) ||
                EF.Functions.ILike(s.Usuario.Apellidos, patron) ||
                EF.Functions.ILike(s.Motivo, patron));
        }

        if (!string.IsNullOrWhiteSpace(filtro.Estado))
        {
            consulta = consulta.Where(s => s.Estado == filtro.Estado);
        }

        if (!string.IsNullOrWhiteSpace(filtro.Area))
        {
            consulta = consulta.Where(s => s.Usuario.Area == filtro.Area);
        }

        if (filtro.EquipoId is not null)
        {
            consulta = consulta.Where(s => s.EquipoId == filtro.EquipoId);
        }

        var total = await consulta.CountAsync();

        var items = await consulta
            .OrderByDescending(s => s.Estado == CatalogoTechAsset.SolicitudPendiente)
            .ThenByDescending(s => s.FechaRegistro)
            .Skip((filtro.Pagina - 1) * filtro.TamanoPagina)
            .Take(filtro.TamanoPagina)
            .ToListAsync();

        return (items, total);
    }

    public async Task<IReadOnlyList<Solicitud>> ObtenerTodasAsync(Guid? usuarioId)
    {
        var consulta = ConsultaBase();
        if (usuarioId is not null)
        {
            consulta = consulta.Where(s => s.UsuarioId == usuarioId);
        }

        return await consulta.OrderByDescending(s => s.FechaRegistro).ToListAsync();
    }

    public async Task<Solicitud?> ObtenerPorIdAsync(Guid id)
        => await ConsultaBase().FirstOrDefaultAsync(s => s.Id == id);

    public async Task<bool> ExistePendientePorEquipoAsync(Guid equipoId)
        => await context.Solicitudes.AnyAsync(s =>
            s.EquipoId == equipoId && s.Estado == CatalogoTechAsset.SolicitudPendiente);

    public async Task<int> ContarPorEstadoAsync(string estado, Guid? usuarioId)
    {
        var consulta = context.Solicitudes.AsNoTracking().AsQueryable();
        if (usuarioId is not null)
        {
            consulta = consulta.Where(s => s.UsuarioId == usuarioId);
        }

        return await consulta.CountAsync(s => s.Estado == estado);
    }

    public async Task AgregarAsync(Solicitud solicitud)
    {
        context.Solicitudes.Add(solicitud);
        await context.SaveChangesAsync();
    }

    public async Task ActualizarAsync(Solicitud solicitud)
    {
        var existente = await context.Solicitudes.FirstOrDefaultAsync(s => s.Id == solicitud.Id);
        if (existente is null)
        {
            return;
        }

        context.Entry(existente).CurrentValues.SetValues(solicitud);
        await context.SaveChangesAsync();
    }

    private IQueryable<Solicitud> ConsultaBase()
        => context.Solicitudes
            .AsNoTracking()
            .Include(s => s.Usuario)
            .Include(s => s.Equipo)
            .Include(s => s.Prestamo)
            .Include(s => s.RevisadoPor)
            .AsQueryable();
}
