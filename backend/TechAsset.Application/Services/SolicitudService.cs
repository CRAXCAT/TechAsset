using TechAsset.Application.DTOs;
using TechAsset.Application.Exceptions;
using TechAsset.Application.Interfaces;
using TechAsset.Application.Models;
using TechAsset.Domain.Constantes;
using TechAsset.Domain.Entities;

namespace TechAsset.Application.Services;

public class SolicitudService : ISolicitudService
{
    private readonly ISolicitudRepository solicitudRepository;
    private readonly IEquipoRepository equipoRepository;
    private readonly IUsuarioRepository usuarioRepository;
    private readonly IPrestamoRepository prestamoRepository;
    private readonly IUnitOfWork unitOfWork;
    private readonly IMovimientoService movimientoService;

    public SolicitudService(
        ISolicitudRepository solicitudRepository,
        IEquipoRepository equipoRepository,
        IUsuarioRepository usuarioRepository,
        IPrestamoRepository prestamoRepository,
        IUnitOfWork unitOfWork,
        IMovimientoService movimientoService)
    {
        this.solicitudRepository = solicitudRepository;
        this.equipoRepository = equipoRepository;
        this.usuarioRepository = usuarioRepository;
        this.prestamoRepository = prestamoRepository;
        this.unitOfWork = unitOfWork;
        this.movimientoService = movimientoService;
    }

    public async Task<ResultadoPaginado<SolicitudDto>> ListarAsync(
        FiltroSolicitudes filtro,
        Guid usuarioId,
        bool esGestor)
    {
        filtro ??= new FiltroSolicitudes();
        filtro.Normalizar();

        if (filtro.Estado is not null && !CatalogoTechAsset.EsEstadoSolicitudValido(filtro.Estado))
        {
            throw new ReglaNegocioException("El estado de la solicitud no es válido.");
        }

        if (filtro.Area is not null && !CatalogoTechAsset.EsAreaValida(filtro.Area))
        {
            throw new ReglaNegocioException("El área solicitada no es válida.");
        }

        var propietario = esGestor ? (Guid?)null : usuarioId;
        var (items, total) = await solicitudRepository.ListarAsync(filtro, propietario);

        return new ResultadoPaginado<SolicitudDto>
        {
            Items = items.Select(s => Mapear(s)).ToList(),
            Total = total,
            Pagina = filtro.Pagina,
            TamanoPagina = filtro.TamanoPagina
        };
    }

    public async Task<SolicitudDto> ObtenerPorIdAsync(Guid id, Guid usuarioId, bool esGestor)
    {
        var solicitud = await solicitudRepository.ObtenerPorIdAsync(id)
            ?? throw new RecursoNoEncontradoException("No se encontró la solicitud indicada.");

        if (!esGestor && solicitud.UsuarioId != usuarioId)
        {
            throw new AccesoDenegadoException("Solo puede consultar sus propias solicitudes.");
        }

        return Mapear(solicitud);
    }

    public async Task<SolicitudDto> CrearAsync(CrearSolicitudDto dto, Guid usuarioId)
    {
        var usuario = await usuarioRepository.ObtenerPorIdAsync(usuarioId)
            ?? throw new RecursoNoEncontradoException("No se encontró el usuario solicitante.");

        if (!usuario.Activo)
        {
            throw new ReglaNegocioException("La cuenta está inactiva y no puede registrar solicitudes.");
        }

        var equipo = await equipoRepository.ObtenerPorIdAsync(dto.EquipoId)
            ?? throw new ReglaNegocioException("El equipo seleccionado no existe.");

        if (equipo.Estado == CatalogoTechAsset.EquipoMantenimiento)
        {
            throw new ReglaNegocioException("No se puede solicitar un equipo en estado Mantenimiento (RN-02).");
        }

        if (equipo.Estado == CatalogoTechAsset.EquipoBaja)
        {
            throw new ReglaNegocioException("No se puede solicitar un equipo en estado Baja (RN-03).");
        }

        if (equipo.Estado != CatalogoTechAsset.EquipoDisponible)
        {
            throw new ReglaNegocioException("El equipo no está disponible para una nueva solicitud.");
        }

        if (await prestamoRepository.ObtenerActivoPorEquipoAsync(equipo.Id) is not null)
        {
            throw new ReglaNegocioException("El equipo ya tiene un préstamo activo (RN-01).");
        }

        if (await solicitudRepository.ExistePendientePorEquipoAsync(equipo.Id))
        {
            throw new ReglaNegocioException("Ya existe una solicitud pendiente para este equipo.");
        }

        ValidarFechas(dto.FechaPrestamo, dto.FechaDevolucion);
        var motivo = Normalizar(dto.Motivo);

        if (motivo.Length < 5)
        {
            throw new ReglaNegocioException("Registre el motivo de la solicitud (mínimo 5 caracteres).");
        }

        var solicitud = new Solicitud
        {
            Id = Guid.NewGuid(),
            FechaPrestamo = dto.FechaPrestamo,
            FechaDevolucion = dto.FechaDevolucion,
            Motivo = motivo,
            Estado = CatalogoTechAsset.SolicitudPendiente,
            UsuarioId = usuario.Id,
            EquipoId = equipo.Id,
            FechaRegistro = DateTime.UtcNow
        };

        await solicitudRepository.AgregarAsync(solicitud);
        await movimientoService.RegistrarAsync(
            "Solicitud",
            solicitud.Id,
            "Crear",
            $"{Codigo(solicitud.Id)} · {equipo.CodigoPatrimonial} · {usuario.Nombres} {usuario.Apellidos}",
            usuario.Id,
            $"{usuario.Nombres} {usuario.Apellidos}".Trim());

        return Mapear(solicitud, usuario, equipo);
    }

    public async Task<SolicitudDto> AprobarAsync(Guid id, string? observacion, Guid revisorId)
    {
        var solicitud = await solicitudRepository.ObtenerPorIdAsync(id)
            ?? throw new RecursoNoEncontradoException("No se encontró la solicitud indicada.");

        if (solicitud.Estado != CatalogoTechAsset.SolicitudPendiente)
        {
            throw new ReglaNegocioException($"La solicitud ya fue {solicitud.Estado.ToLowerInvariant()}.");
        }

        var revisor = await usuarioRepository.ObtenerPorIdAsync(revisorId)
            ?? throw new RecursoNoEncontradoException("No se encontró el responsable de la revisión.");

        if (!revisor.Activo || revisor.Rol == CatalogoTechAsset.RolColaborador)
        {
            throw new AccesoDenegadoException("Solo el Responsable de Tecnología o el Administrador pueden aprobar solicitudes.");
        }

        var equipo = solicitud.Equipo
            ?? await equipoRepository.ObtenerPorIdAsync(solicitud.EquipoId)
            ?? throw new ReglaNegocioException("El equipo de la solicitud ya no existe.");

        if (equipo.Estado != CatalogoTechAsset.EquipoDisponible)
        {
            throw new ReglaNegocioException("El equipo ya no está disponible para aprobar la solicitud.");
        }

        if (await prestamoRepository.ObtenerActivoPorEquipoAsync(equipo.Id) is not null)
        {
            throw new ReglaNegocioException("El equipo ya tiene un préstamo activo (RN-01).");
        }

        ValidarFechas(solicitud.FechaPrestamo, solicitud.FechaDevolucion);

        var prestamo = new Prestamo
        {
            Id = Guid.NewGuid(),
            FechaPrestamo = solicitud.FechaPrestamo,
            FechaDevolucion = solicitud.FechaDevolucion,
            Observacion = solicitud.Motivo,
            Estado = CatalogoTechAsset.PrestamoActivo,
            UsuarioId = solicitud.UsuarioId,
            EquipoId = solicitud.EquipoId,
            ResponsableId = revisor.Id,
            FechaRegistro = DateTime.UtcNow
        };

        solicitud.Estado = CatalogoTechAsset.SolicitudAprobada;
        solicitud.PrestamoId = prestamo.Id;
        solicitud.RevisadoPorId = revisor.Id;
        solicitud.FechaRevision = DateTime.UtcNow;
        solicitud.ObservacionRevision = Normalizar(observacion);
        equipo.Estado = CatalogoTechAsset.EquipoPrestado;

        await unitOfWork.EjecutarAsync(async () =>
        {
            await prestamoRepository.AgregarAsync(prestamo);
            await equipoRepository.ActualizarAsync(equipo);
            await solicitudRepository.ActualizarAsync(solicitud);
            await movimientoService.RegistrarAsync(
                "Solicitud",
                solicitud.Id,
                "Aprobar",
                $"{Codigo(solicitud.Id)} · {equipo.CodigoPatrimonial} · préstamo {CodigoPrestamo(prestamo.Id)}",
                revisor.Id,
                $"{revisor.Nombres} {revisor.Apellidos}".Trim());
            return true;
        });

        var actualizada = await solicitudRepository.ObtenerPorIdAsync(solicitud.Id) ?? solicitud;
        return Mapear(actualizada);
    }

    public async Task<SolicitudDto> RechazarAsync(Guid id, string observacion, Guid revisorId)
    {
        var solicitud = await solicitudRepository.ObtenerPorIdAsync(id)
            ?? throw new RecursoNoEncontradoException("No se encontró la solicitud indicada.");

        if (solicitud.Estado != CatalogoTechAsset.SolicitudPendiente)
        {
            throw new ReglaNegocioException($"La solicitud ya fue {solicitud.Estado.ToLowerInvariant()}.");
        }

        var detalle = Normalizar(observacion);
        if (detalle.Length < 5)
        {
            throw new ReglaNegocioException("Todo rechazo debe registrar una observación (mínimo 5 caracteres).");
        }

        var revisor = await usuarioRepository.ObtenerPorIdAsync(revisorId)
            ?? throw new RecursoNoEncontradoException("No se encontró el responsable de la revisión.");

        if (!revisor.Activo || revisor.Rol == CatalogoTechAsset.RolColaborador)
        {
            throw new AccesoDenegadoException("Solo el Responsable de Tecnología o el Administrador pueden rechazar solicitudes.");
        }

        solicitud.Estado = CatalogoTechAsset.SolicitudRechazada;
        solicitud.RevisadoPorId = revisor.Id;
        solicitud.FechaRevision = DateTime.UtcNow;
        solicitud.ObservacionRevision = detalle;
        solicitud.PrestamoId = null;

        await solicitudRepository.ActualizarAsync(solicitud);
        await movimientoService.RegistrarAsync(
            "Solicitud",
            solicitud.Id,
            "Rechazar",
            $"{Codigo(solicitud.Id)} · {solicitud.Equipo?.CodigoPatrimonial ?? string.Empty} · {detalle}",
            revisor.Id,
            $"{revisor.Nombres} {revisor.Apellidos}".Trim());

        var actualizada = await solicitudRepository.ObtenerPorIdAsync(solicitud.Id) ?? solicitud;
        return Mapear(actualizada);
    }

    private static void ValidarFechas(DateOnly fechaPrestamo, DateOnly fechaDevolucion)
    {
        if (fechaPrestamo < DateOnly.FromDateTime(DateTime.Today))
        {
            throw new ReglaNegocioException("La fecha de préstamo no puede ser anterior a hoy.");
        }

        if (fechaDevolucion <= fechaPrestamo)
        {
            throw new ReglaNegocioException("La fecha de devolución debe ser posterior a la fecha de préstamo (RN-04).");
        }
    }

    private static string Normalizar(string? valor)
        => string.IsNullOrWhiteSpace(valor)
            ? string.Empty
            : string.Join(' ', valor.Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries));

    private static string Codigo(Guid id) => $"SOL-{id.ToString("N")[..6].ToUpperInvariant()}";

    private static string CodigoPrestamo(Guid id) => $"PR-{id.ToString("N")[..6].ToUpperInvariant()}";

    private static SolicitudDto Mapear(Solicitud solicitud, Usuario? usuario = null, Equipo? equipo = null) => new()
    {
        Id = solicitud.Id,
        Codigo = Codigo(solicitud.Id),
        FechaPrestamo = solicitud.FechaPrestamo,
        FechaDevolucion = solicitud.FechaDevolucion,
        Motivo = solicitud.Motivo,
        Estado = solicitud.Estado,
        ObservacionRevision = solicitud.ObservacionRevision,
        UsuarioId = solicitud.UsuarioId,
        Solicitante = (usuario ?? solicitud.Usuario) is null
            ? string.Empty
            : $"{(usuario ?? solicitud.Usuario)!.Nombres} {(usuario ?? solicitud.Usuario)!.Apellidos}".Trim(),
        Area = (usuario ?? solicitud.Usuario)?.Area ?? string.Empty,
        EquipoId = solicitud.EquipoId,
        Equipo = (equipo ?? solicitud.Equipo)?.Nombre ?? string.Empty,
        CodigoPatrimonial = (equipo ?? solicitud.Equipo)?.CodigoPatrimonial ?? string.Empty,
        Categoria = (equipo ?? solicitud.Equipo)?.Categoria ?? string.Empty,
        PrestamoId = solicitud.PrestamoId,
        CodigoPrestamo = solicitud.PrestamoId is null ? null : CodigoPrestamo(solicitud.PrestamoId.Value),
        RevisadoPorId = solicitud.RevisadoPorId,
        Revisor = solicitud.RevisadoPor is null
            ? null
            : $"{solicitud.RevisadoPor.Nombres} {solicitud.RevisadoPor.Apellidos}".Trim(),
        FechaRegistro = solicitud.FechaRegistro,
        FechaRevision = solicitud.FechaRevision
    };
}
