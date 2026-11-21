using TechAsset.Application.DTOs;
using TechAsset.Application.Exceptions;
using TechAsset.Application.Interfaces;
using TechAsset.Application.Models;
using TechAsset.Domain.Constantes;
using TechAsset.Domain.Entities;

namespace TechAsset.Application.Services;

public class PrestamoService : IPrestamoService
{
    private readonly IPrestamoRepository prestamoRepository;
    private readonly IUsuarioRepository usuarioRepository;
    private readonly IEquipoRepository equipoRepository;
    private readonly ISolicitudRepository solicitudRepository;
    private readonly IUnitOfWork unitOfWork;
    private readonly IMovimientoService movimientoService;

    public PrestamoService(
        IPrestamoRepository prestamoRepository,
        IUsuarioRepository usuarioRepository,
        IEquipoRepository equipoRepository,
        ISolicitudRepository solicitudRepository,
        IUnitOfWork unitOfWork,
        IMovimientoService movimientoService)
    {
        this.prestamoRepository = prestamoRepository;
        this.usuarioRepository = usuarioRepository;
        this.equipoRepository = equipoRepository;
        this.solicitudRepository = solicitudRepository;
        this.unitOfWork = unitOfWork;
        this.movimientoService = movimientoService;
    }

    public async Task<ResultadoPaginado<PrestamoDto>> ListarAsync(
        FiltroPrestamos filtro,
        Guid? usuarioId,
        bool esGestor)
    {
        filtro ??= new FiltroPrestamos();
        filtro.Normalizar();

        if (filtro.Estado is not null && !CatalogoTechAsset.EsEstadoPrestamoValido(filtro.Estado))
        {
            throw new ReglaNegocioException("El estado del préstamo no es válido.");
        }

        if (filtro.Area is not null && !CatalogoTechAsset.EsAreaValida(filtro.Area))
        {
            throw new ReglaNegocioException("El área solicitada no es válida.");
        }

        var propietario = esGestor ? (Guid?)null : usuarioId;
        var (items, total) = await prestamoRepository.ListarAsync(filtro, propietario);

        return new ResultadoPaginado<PrestamoDto>
        {
            Items = items.Select(p => Mapear(p)).ToList(),
            Total = total,
            Pagina = filtro.Pagina,
            TamanoPagina = filtro.TamanoPagina
        };
    }

    public async Task<PrestamoDto> ObtenerPorIdAsync(Guid id, Guid? usuarioId, bool esGestor)
    {
        var prestamo = await prestamoRepository.ObtenerPorIdAsync(id)
            ?? throw new RecursoNoEncontradoException("No se encontró el préstamo solicitado.");

        if (!esGestor && prestamo.UsuarioId != usuarioId)
        {
            throw new AccesoDenegadoException("Solo puede consultar sus propios préstamos.");
        }

        return Mapear(prestamo);
    }

    public async Task<PrestamoDto> CrearAsync(CrearPrestamoDto dto, Guid responsableId)
    {
        var usuario = await usuarioRepository.ObtenerPorIdAsync(dto.UsuarioId)
            ?? throw new ReglaNegocioException("El colaborador seleccionado no existe.");

        if (!usuario.Activo)
        {
            throw new ReglaNegocioException("El colaborador está inactivo y no puede recibir préstamos.");
        }

        var equipo = await equipoRepository.ObtenerPorIdAsync(dto.EquipoId)
            ?? throw new ReglaNegocioException("El equipo seleccionado no existe.");

        if (equipo.Estado == CatalogoTechAsset.EquipoMantenimiento)
        {
            throw new ReglaNegocioException("No se puede prestar un equipo en estado Mantenimiento (RN-02).");
        }

        if (equipo.Estado == CatalogoTechAsset.EquipoBaja)
        {
            throw new ReglaNegocioException("No se puede prestar un equipo en estado Baja (RN-03).");
        }

        if (await prestamoRepository.ObtenerActivoPorEquipoAsync(equipo.Id) is not null)
        {
            throw new ReglaNegocioException("El equipo ya tiene un préstamo activo (RN-01).");
        }

        if (dto.FechaDevolucion <= dto.FechaPrestamo)
        {
            throw new ReglaNegocioException("La fecha de devolución debe ser posterior a la fecha de préstamo (RN-04).");
        }

        var observacion = Normalizar(dto.Observacion);
        if (observacion.Length < 5)
        {
            throw new ReglaNegocioException("Registre el motivo del préstamo (mínimo 5 caracteres).");
        }

        var responsable = await usuarioRepository.ObtenerPorIdAsync(responsableId)
            ?? throw new ReglaNegocioException("No se encontró el responsable que registra el préstamo (RN-05).");

        if (!responsable.Activo || responsable.Rol == CatalogoTechAsset.RolColaborador)
        {
            throw new ReglaNegocioException("Solo el Responsable de Tecnología o el Administrador pueden registrar préstamos (RN-05).");
        }

        var prestamo = new Prestamo
        {
            Id = Guid.NewGuid(),
            FechaPrestamo = dto.FechaPrestamo,
            FechaDevolucion = dto.FechaDevolucion,
            Observacion = observacion,
            Estado = CatalogoTechAsset.PrestamoActivo,
            UsuarioId = usuario.Id,
            EquipoId = equipo.Id,
            ResponsableId = responsable.Id,
            FechaRegistro = DateTime.UtcNow
        };

        equipo.Estado = CatalogoTechAsset.EquipoPrestado;

        await unitOfWork.EjecutarAsync(async () =>
        {
            await prestamoRepository.AgregarAsync(prestamo);
            await equipoRepository.ActualizarAsync(equipo);
            await movimientoService.RegistrarAsync(
                "Prestamo",
                prestamo.Id,
                "Registrar",
                $"{Codigo(prestamo.Id)} · {equipo.CodigoPatrimonial} · {usuario.Nombres} {usuario.Apellidos}",
                responsable.Id,
                $"{responsable.Nombres} {responsable.Apellidos}".Trim());
            return true;
        });

        return Mapear(prestamo, usuario, equipo, responsable);
    }

    public async Task<PrestamoDto> DevolverAsync(Guid id, string observacion, Guid usuarioId)
    {
        var prestamo = await prestamoRepository.ObtenerPorIdAsync(id)
            ?? throw new RecursoNoEncontradoException("No se encontró el préstamo solicitado.");

        if (prestamo.Estado != CatalogoTechAsset.PrestamoActivo)
        {
            throw new ReglaNegocioException("El préstamo ya fue devuelto.");
        }

        var detalle = Normalizar(observacion);
        if (detalle.Length < 5)
        {
            throw new ReglaNegocioException("Toda devolución debe registrar observaciones (RN-10).");
        }

        prestamo.Estado = CatalogoTechAsset.PrestamoDevuelto;
        prestamo.FechaDevolucionReal = DateOnly.FromDateTime(DateTime.Today);
        prestamo.ObservacionDevolucion = detalle;

        if (prestamo.Equipo is not null)
        {
            prestamo.Equipo.Estado = CatalogoTechAsset.EquipoDisponible;
        }

        var actor = await usuarioRepository.ObtenerPorIdAsync(usuarioId);

        await unitOfWork.EjecutarAsync(async () =>
        {
            await prestamoRepository.ActualizarAsync(prestamo);
            if (prestamo.Equipo is not null)
            {
                await equipoRepository.ActualizarAsync(prestamo.Equipo);
            }

            await movimientoService.RegistrarAsync(
                "Prestamo",
                prestamo.Id,
                "Devolver",
                $"{Codigo(prestamo.Id)} · {prestamo.Equipo?.CodigoPatrimonial ?? string.Empty} · devolución registrada",
                usuarioId,
                actor is null ? "Usuario" : $"{actor.Nombres} {actor.Apellidos}".Trim());
            return true;
        });

        return Mapear(prestamo);
    }

    public async Task<ResumenTechAssetDto> ObtenerResumenAsync(Guid? usuarioId, bool esGestor)
    {
        var propietario = esGestor ? (Guid?)null : usuarioId;
        var equipos = await equipoRepository.ObtenerTodosAsync();
        var prestamos = await prestamoRepository.ObtenerTodosAsync(propietario);
        var solicitudes = await solicitudRepository.ObtenerTodasAsync(propietario);

        var porArea = prestamos
            .GroupBy(p => p.Usuario?.Area ?? "Sin área")
            .Select(g => new UsoDto { Etiqueta = g.Key, Total = g.Count() })
            .OrderByDescending(x => x.Total)
            .ThenBy(x => x.Etiqueta)
            .ToList();

        var porEstado = equipos
            .GroupBy(e => e.Estado)
            .Select(g => new UsoDto { Etiqueta = g.Key, Total = g.Count() })
            .OrderByDescending(x => x.Total)
            .ToList();

        var masUtilizados = prestamos
            .GroupBy(p => p.Equipo?.Nombre ?? "Sin equipo")
            .Select(g => new UsoDto { Etiqueta = g.Key, Total = g.Count() })
            .OrderByDescending(x => x.Total)
            .ThenBy(x => x.Etiqueta)
            .Take(6)
            .ToList();

        var areaMayor = porArea.FirstOrDefault();

        return new ResumenTechAssetDto
        {
            TotalEquipos = equipos.Count,
            Disponibles = equipos.Count(e => e.Estado == CatalogoTechAsset.EquipoDisponible),
            Prestados = equipos.Count(e => e.Estado == CatalogoTechAsset.EquipoPrestado),
            Mantenimiento = equipos.Count(e => e.Estado == CatalogoTechAsset.EquipoMantenimiento),
            Bajas = equipos.Count(e => e.Estado == CatalogoTechAsset.EquipoBaja),
            TotalPrestamos = prestamos.Count,
            PrestamosActivos = prestamos.Count(p => p.Estado == CatalogoTechAsset.PrestamoActivo),
            PrestamosDevueltos = prestamos.Count(p => p.Estado == CatalogoTechAsset.PrestamoDevuelto),
            TotalSolicitudes = solicitudes.Count,
            SolicitudesPendientes = solicitudes.Count(s => s.Estado == CatalogoTechAsset.SolicitudPendiente),
            SolicitudesAprobadas = solicitudes.Count(s => s.Estado == CatalogoTechAsset.SolicitudAprobada),
            SolicitudesRechazadas = solicitudes.Count(s => s.Estado == CatalogoTechAsset.SolicitudRechazada),
            AreaMayorUso = areaMayor?.Etiqueta ?? "Sin datos",
            PrestamosAreaMayor = areaMayor?.Total ?? 0,
            PrestamosPorArea = porArea,
            EquiposPorEstado = porEstado,
            EquiposMasUtilizados = masUtilizados
        };
    }

    private static string Normalizar(string? valor)
        => string.IsNullOrWhiteSpace(valor)
            ? string.Empty
            : string.Join(' ', valor.Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries));

    private static string Codigo(Guid id) => $"PR-{id.ToString("N")[..6].ToUpperInvariant()}";

    private static PrestamoDto Mapear(
        Prestamo prestamo,
        Usuario? usuario = null,
        Equipo? equipo = null,
        Usuario? responsable = null) => new()
    {
        Id = prestamo.Id,
        Codigo = Codigo(prestamo.Id),
        FechaPrestamo = prestamo.FechaPrestamo,
        FechaDevolucion = prestamo.FechaDevolucion,
        FechaDevolucionReal = prestamo.FechaDevolucionReal,
        Observacion = prestamo.Observacion,
        ObservacionDevolucion = prestamo.ObservacionDevolucion,
        Estado = prestamo.Estado,
        UsuarioId = prestamo.UsuarioId,
        Solicitante = (usuario ?? prestamo.Usuario) is null ? string.Empty : $"{(usuario ?? prestamo.Usuario)!.Nombres} {(usuario ?? prestamo.Usuario)!.Apellidos}".Trim(),
        Area = (usuario ?? prestamo.Usuario)?.Area ?? string.Empty,
        EquipoId = prestamo.EquipoId,
        Equipo = (equipo ?? prestamo.Equipo)?.Nombre ?? string.Empty,
        CodigoPatrimonial = (equipo ?? prestamo.Equipo)?.CodigoPatrimonial ?? string.Empty,
        Categoria = (equipo ?? prestamo.Equipo)?.Categoria ?? string.Empty,
        ResponsableId = prestamo.ResponsableId,
        Responsable = (responsable ?? prestamo.Responsable) is null ? string.Empty : $"{(responsable ?? prestamo.Responsable)!.Nombres} {(responsable ?? prestamo.Responsable)!.Apellidos}".Trim(),
        FechaRegistro = prestamo.FechaRegistro
    };
}
