namespace TechAsset.Application.Interfaces;

/// <summary>
/// Ejecuta un conjunto de operaciones dentro de una misma transacción de base
/// de datos. Permite que el préstamo y el estado del equipo se confirmen juntos.
/// </summary>
public interface IUnitOfWork
{
    Task<T> EjecutarAsync<T>(Func<Task<T>> operacion);
}
