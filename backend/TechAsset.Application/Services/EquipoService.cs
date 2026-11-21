using TechAsset.Application.DTOs;
using TechAsset.Application.Exceptions;
using TechAsset.Application.Interfaces;
using TechAsset.Application.Models;
using TechAsset.Domain.Constantes;
using TechAsset.Domain.Entities;

namespace TechAsset.Application.Services;

public class EquipoService : IEquipoService
{
    private readonly IEquipoRepository equipoRepository;

    public EquipoService(IEquipoRepository equipoRepository)
    {
        this.equipoRepository = equipoRepository;
    }

    public async Task<IReadOnlyList<EquipoDto>> ListarAsync(FiltroEquipos filtro)
    {
        filtro ??= new FiltroEquipos();
        filtro.Normalizar();

        if (filtro.Categoria is not null && !CatalogoTechAsset.EsCategoriaValida(filtro.Categoria))
        {
            throw new ReglaNegocioException("La categoría solicitada no es válida.");
        }

        if (filtro.Estado is not null && !CatalogoTechAsset.EsEstadoEquipoValido(filtro.Estado))
        {
            throw new ReglaNegocioException("El estado solicitado no es válido.");
        }

        var equipos = await equipoRepository.ListarAsync(filtro);
        return equipos.Select(Mapear).ToList();
    }

    public async Task<IReadOnlyList<EquipoDto>> ObtenerTodosAsync()
    {
        var equipos = await equipoRepository.ObtenerTodosAsync();
        return equipos.Select(Mapear).ToList();
    }

    public async Task<EquipoDto> ObtenerPorIdAsync(Guid id)
    {
        var equipo = await equipoRepository.ObtenerPorIdAsync(id)
            ?? throw new RecursoNoEncontradoException("No se encontró el equipo solicitado.");
        return Mapear(equipo);
    }

    public async Task<EquipoDto> CrearAsync(CrearEquipoDto dto)
    {
        var equipo = await ConstruirAsync(dto, null);
        await equipoRepository.AgregarAsync(equipo);

        var creado = await equipoRepository.ObtenerPorIdAsync(equipo.Id);
        return Mapear(creado ?? equipo);
    }

    public async Task<EquipoDto> ActualizarAsync(Guid id, CrearEquipoDto dto)
    {
        var existente = await equipoRepository.ObtenerPorIdAsync(id)
            ?? throw new RecursoNoEncontradoException("No se encontró el equipo solicitado.");

        var actualizado = await ConstruirAsync(dto, id);
        var prestamoActivo = await equipoRepository.TienePrestamosAsync(id);

        if (prestamoActivo && actualizado.Estado != CatalogoTechAsset.EquipoPrestado)
        {
            throw new ReglaNegocioException(
                "El equipo tiene un préstamo activo. Registre la devolución antes de cambiar su estado.");
        }

        if (!prestamoActivo && actualizado.Estado == CatalogoTechAsset.EquipoPrestado)
        {
            throw new ReglaNegocioException("El estado Prestado solo se asigna al registrar un préstamo.");
        }

        existente.CodigoPatrimonial = actualizado.CodigoPatrimonial;
        existente.Nombre = actualizado.Nombre;
        existente.Categoria = actualizado.Categoria;
        existente.Marca = actualizado.Marca;
        existente.Estado = actualizado.Estado;

        await equipoRepository.ActualizarAsync(existente);
        return Mapear(existente);
    }

    public async Task<EquipoDto> CambiarEstadoAsync(Guid id, string estado)
    {
        var equipo = await equipoRepository.ObtenerPorIdAsync(id)
            ?? throw new RecursoNoEncontradoException("No se encontró el equipo solicitado.");

        var nuevoEstado = string.IsNullOrWhiteSpace(estado) ? string.Empty : estado.Trim();

        if (!CatalogoTechAsset.EsEstadoEquipoValido(nuevoEstado))
        {
            throw new ReglaNegocioException("El estado indicado no es válido.");
        }

        if (nuevoEstado == CatalogoTechAsset.EquipoPrestado)
        {
            throw new ReglaNegocioException("El estado Prestado solo se asigna al registrar un préstamo.");
        }

        var prestamoActivo = await equipoRepository.TienePrestamosAsync(id);
        if (prestamoActivo)
        {
            throw new ReglaNegocioException(
                "El equipo tiene un préstamo activo. Registre la devolución antes de cambiar su estado.");
        }

        equipo.Estado = nuevoEstado;
        await equipoRepository.ActualizarAsync(equipo);
        return Mapear(equipo);
    }

    public async Task EliminarAsync(Guid id)
    {
        var equipo = await equipoRepository.ObtenerPorIdAsync(id)
            ?? throw new RecursoNoEncontradoException("No se encontró el equipo solicitado.");

        if (await equipoRepository.TienePrestamosAsync(id))
        {
            throw new ReglaNegocioException(
                "No se puede eliminar un equipo con historial de préstamos (RN-06). Puede marcarlo como Baja.");
        }

        await equipoRepository.EliminarAsync(equipo);
    }

    private async Task<Equipo> ConstruirAsync(CrearEquipoDto dto, Guid? excluirId)
    {
        var codigo = Normalizar(dto.CodigoPatrimonial).ToUpperInvariant();
        var nombre = Normalizar(dto.Nombre);
        var categoria = Normalizar(dto.Categoria);
        var marca = Normalizar(dto.Marca);
        var estado = Normalizar(dto.Estado);

        if (!CatalogoTechAsset.EsCategoriaValida(categoria))
        {
            throw new ReglaNegocioException("La categoría seleccionada no es válida.");
        }

        if (!CatalogoTechAsset.EsEstadoEquipoValido(estado))
        {
            throw new ReglaNegocioException("El estado seleccionado no es válido.");
        }

        if (estado == CatalogoTechAsset.EquipoPrestado)
        {
            throw new ReglaNegocioException("El estado Prestado solo se asigna al registrar un préstamo.");
        }

        if (await equipoRepository.ExisteCodigoAsync(codigo, excluirId))
        {
            throw new ReglaNegocioException("Ya existe un equipo con ese código patrimonial (RN-07).");
        }

        return new Equipo
        {
            Id = Guid.NewGuid(),
            CodigoPatrimonial = codigo,
            Nombre = nombre,
            Categoria = categoria,
            Marca = marca,
            Estado = estado,
            FechaRegistro = DateTime.UtcNow
        };
    }

    private static string Normalizar(string? valor)
        => string.IsNullOrWhiteSpace(valor)
            ? string.Empty
            : string.Join(' ', valor.Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries));

    private static EquipoDto Mapear(Equipo equipo)
    {
        var prestamos = equipo.Prestamos ?? new List<Prestamo>();
        return new EquipoDto
        {
            Id = equipo.Id,
            CodigoPatrimonial = equipo.CodigoPatrimonial,
            Nombre = equipo.Nombre,
            Categoria = equipo.Categoria,
            Marca = equipo.Marca,
            Estado = equipo.Estado,
            PrestamoActivo = prestamos.Any(p => p.Estado == CatalogoTechAsset.PrestamoActivo),
            TotalPrestamos = prestamos.Count,
            FechaRegistro = equipo.FechaRegistro
        };
    }
}
