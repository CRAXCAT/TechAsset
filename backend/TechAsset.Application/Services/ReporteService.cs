using System.Globalization;
using System.Text;
using TechAsset.Application.DTOs;
using TechAsset.Application.Interfaces;
using TechAsset.Application.Models;

namespace TechAsset.Application.Services;

public class ReporteService : IReporteService
{
    private readonly IPrestamoService prestamoService;
    private readonly IPrestamoRepository prestamoRepository;
    private readonly IEquipoRepository equipoRepository;

    public ReporteService(
        IPrestamoService prestamoService,
        IPrestamoRepository prestamoRepository,
        IEquipoRepository equipoRepository)
    {
        this.prestamoService = prestamoService;
        this.prestamoRepository = prestamoRepository;
        this.equipoRepository = equipoRepository;
    }

    public Task<ResumenTechAssetDto> ObtenerResumenAsync(Guid? usuarioId, bool esGestor)
        => prestamoService.ObtenerResumenAsync(usuarioId, esGestor);

    public async Task<byte[]> ExportarPrestamosCsvAsync(FiltroPrestamos filtro, Guid? usuarioId, bool esGestor)
    {
        filtro ??= new FiltroPrestamos();
        filtro.TamanoPagina = 1000;
        filtro.Pagina = 1;
        filtro.Normalizar();

        var propietario = esGestor ? (Guid?)null : usuarioId;
        var (items, _) = await prestamoRepository.ListarAsync(filtro, propietario);
        var lineas = new List<string>
        {
            "Codigo;Equipo;CodigoPatrimonial;Solicitante;Area;FechaPrestamo;FechaDevolucion;FechaDevolucionReal;Estado;Observacion"
        };

        foreach (var p in items)
        {
            lineas.Add(string.Join(';', new[]
            {
                $"PR-{p.Id.ToString("N")[..6].ToUpperInvariant()}",
                Limpiar(p.Equipo?.Nombre),
                Limpiar(p.Equipo?.CodigoPatrimonial),
                Limpiar($"{p.Usuario?.Nombres} {p.Usuario?.Apellidos}"),
                Limpiar(p.Usuario?.Area),
                p.FechaPrestamo.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture),
                p.FechaDevolucion.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture),
                p.FechaDevolucionReal?.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture) ?? "",
                p.Estado,
                Limpiar(p.Observacion)
            }));
        }

        return Encoding.UTF8.GetPreamble().Concat(Encoding.UTF8.GetBytes(string.Join(Environment.NewLine, lineas))).ToArray();
    }

    public async Task<byte[]> ExportarEquiposCsvAsync(FiltroEquipos filtro)
    {
        filtro ??= new FiltroEquipos();
        var equipos = await equipoRepository.ListarAsync(filtro);
        var lineas = new List<string> { "CodigoPatrimonial;Equipo;Categoria;Marca;Estado;Prestamos" };

        foreach (var e in equipos)
        {
            lineas.Add(string.Join(';', new[]
            {
                Limpiar(e.CodigoPatrimonial),
                Limpiar(e.Nombre),
                Limpiar(e.Categoria),
                Limpiar(e.Marca),
                e.Estado,
                (e.Prestamos?.Count ?? 0).ToString(CultureInfo.InvariantCulture)
            }));
        }

        return Encoding.UTF8.GetPreamble().Concat(Encoding.UTF8.GetBytes(string.Join(Environment.NewLine, lineas))).ToArray();
    }

    private static string Limpiar(string? valor)
        => string.IsNullOrWhiteSpace(valor) ? string.Empty : valor.Replace(';', ',').Trim();
}
